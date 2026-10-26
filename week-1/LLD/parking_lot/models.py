from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum


class VehicleType(str, Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    TRUCK = "TRUCK"


@dataclass(frozen=True)
class Vehicle:
    plate: str
    kind: VehicleType

    @classmethod
    def create(cls, plate, kind):
        """Factory validates external strings before producing a domain value."""
        plate = plate.strip().upper()
        if not plate:
            raise ValueError("Plate must not be empty")
        return cls(plate, VehicleType(kind.strip().upper()))


@dataclass
class ParkingSlot:
    floor: int
    slot_id: str
    kind: VehicleType
    ticket_id: str | None = None


@dataclass
class ParkingFloor:
    number: int
    slots: dict[str, ParkingSlot] = field(default_factory=dict)


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    vehicle: Vehicle
    floor: int
    slot_id: str
    entered_at: datetime
    exited_at: datetime | None = None
    fee: Decimal = Decimal("0")

    @property
    def active(self):
        return self.exited_at is None
