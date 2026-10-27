"""Public service boundary; all state changes happen under one process lock."""
from dataclasses import replace
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
from threading import RLock
from uuid import uuid4
from .models import ParkingFloor, ParkingSlot, Ticket, Vehicle, VehicleType
from .strategies import LowestFloor, HourlyFee


def utc_now():
    return datetime.now(timezone.utc)


def check_time(value):
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Use timezone-aware datetimes")


class ParkingLot:
    def __init__(self, name, allocation=None, pricing=None, clock=utc_now):
        if not name.strip():
            raise ValueError("Lot name must not be empty")
        self.name = name
        self._floors = {}
        self._tickets = {}
        self._plates = {}
        self._ticket_pricing = {}
        self._allocation = LowestFloor() if allocation is None else allocation
        self._pricing = HourlyFee() if pricing is None else pricing
        self._clock = clock
        self._lock = RLock()

    def add_floor(self, number):
        with self._lock:
            if type(number) is not int or number < 1 or number in self._floors:
                raise ValueError("Floor must be positive and unique")
            self._floors[number] = ParkingFloor(number)

    def add_slot(self, floor, slot_id, kind):
        kind = VehicleType(kind.strip().upper())
        slot_id = slot_id.strip()
        with self._lock:
            if type(floor) is not int or floor not in self._floors:
                raise ValueError("Unknown floor")
            slots = self._floors[floor].slots
            if not slot_id or slot_id in slots:
                raise ValueError("Slot id must be nonempty and unique on its floor")
            slots[slot_id] = ParkingSlot(floor, slot_id, kind)

    def set_strategies(self, allocation=None, pricing=None):
        """New pricing applies to future tickets; existing tickets retain their rule."""
        with self._lock:
            if allocation is not None:
                self._allocation = allocation
            if pricing is not None:
                self._pricing = pricing

    def _available(self, kind=None):
        return [slot for floor in self._floors.values() for slot in floor.slots.values()
                if slot.ticket_id is None and (kind is None or slot.kind == kind)]

    def free_slots(self, kind=None):
        kind = VehicleType(kind.strip().upper()) if kind is not None else None
        with self._lock:
            # Return copies; callers must not mutate live allocation state.
            return [replace(s) for s in sorted(self._available(kind), key=lambda s: (s.floor, s.slot_id))]

    def park(self, plate, kind, entered_at=None):
        vehicle = Vehicle.create(plate, kind)
        entered_at = self._clock() if entered_at is None else entered_at
        check_time(entered_at)
        entered_at = entered_at.astimezone(timezone.utc)
        with self._lock:
            if vehicle.plate in self._plates:
                raise ValueError("Vehicle already parked")
            available = self._available(vehicle.kind)
            # Strategies see detached candidates, never mutable live occupancy.
            candidates = [replace(slot) for slot in available]
            selected = self._allocation.choose(candidates)
            if selected is None:
                raise ValueError("No compatible free slot")
            position = next((i for i, candidate in enumerate(candidates)
                             if candidate is selected), None)
            if position is None or selected != available[position]:
                raise ValueError("Allocation strategy returned an invalid slot")
            slot = available[position]
            # Snapshot before changing any state; strategies must be deepcopy-safe.
            pricing = deepcopy(self._pricing)
            ticket_id = uuid4().hex
            ticket = Ticket(ticket_id, vehicle, slot.floor, slot.slot_id, entered_at)
            slot.ticket_id = ticket_id
            self._tickets[ticket_id] = ticket
            self._plates[vehicle.plate] = ticket_id
            self._ticket_pricing[ticket_id] = pricing
            return ticket

    def unpark(self, ticket_id, exited_at=None):
        exited_at = self._clock() if exited_at is None else exited_at
        check_time(exited_at)
        exited_at = exited_at.astimezone(timezone.utc)
        with self._lock:
            ticket = self._tickets.get(ticket_id)
            if ticket is None or not ticket.active:
                raise ValueError("Unknown or already closed ticket")
            if exited_at < ticket.entered_at:
                raise ValueError("Exit time precedes entry")
            # Validate and calculate before mutating any occupancy/ticket state.
            fee = self._ticket_pricing[ticket_id].calculate(ticket.vehicle.kind, ticket.entered_at, exited_at)
            if not isinstance(fee, Decimal) or not fee.is_finite() or fee < 0:
                raise ValueError("Fee strategy returned an invalid amount")
            slot = self._floors[ticket.floor].slots[ticket.slot_id]
            if slot.ticket_id != ticket_id:
                raise RuntimeError("Ticket and occupancy disagree")
            closed = replace(ticket, exited_at=exited_at, fee=fee)
            self._tickets[ticket_id] = closed
            slot.ticket_id = None
            del self._plates[ticket.vehicle.plate]
            del self._ticket_pricing[ticket_id]
            return closed

    def occupancy(self):
        with self._lock:
            result = {}
            for number, floor in sorted(self._floors.items()):
                result[number] = {}
                for kind in VehicleType:
                    slots = [s for s in floor.slots.values() if s.kind == kind]
                    used = sum(s.ticket_id is not None for s in slots)
                    result[number][kind.value] = {"total": len(slots), "occupied": used, "free": len(slots) - used}
            return result
