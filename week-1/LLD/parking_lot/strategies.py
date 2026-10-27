"""Replaceable allocation and fee rules. Amounts are illustrative INR rates."""
from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import timezone
from math import ceil
from .models import VehicleType


class AllocationStrategy(ABC):
    @abstractmethod
    def choose(self, available):
        """Return one available slot or None."""


class LowestFloor(AllocationStrategy):
    def choose(self, available):
        return min(available, key=lambda s: (s.floor, s.slot_id), default=None)


class HighestFloor(AllocationStrategy):
    def choose(self, available):
        return min(available, key=lambda s: (-s.floor, s.slot_id), default=None)


class FeeStrategy(ABC):
    @abstractmethod
    def calculate(self, kind, entered_at, exited_at):
        """Return a nonnegative Decimal fee."""


def billable_hours(entered_at, exited_at):
    for value in (entered_at, exited_at):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Use timezone-aware datetimes")
    seconds = (exited_at.astimezone(timezone.utc) - entered_at.astimezone(timezone.utc)).total_seconds()
    if seconds < 0:
        raise ValueError("Exit time precedes entry")
    return max(1, ceil(seconds / 3600))


class HourlyFee(FeeStrategy):
    RATES = {VehicleType.BIKE: Decimal("10"), VehicleType.CAR: Decimal("20"), VehicleType.TRUCK: Decimal("50")}

    def __init__(self):
        self.RATES = dict(type(self).RATES)

    def calculate(self, kind, entered_at, exited_at):
        return self.RATES[kind] * billable_hours(entered_at, exited_at)


class TieredFee(FeeStrategy):
    EXTRA = {VehicleType.BIKE: Decimal("5"), VehicleType.CAR: Decimal("15"), VehicleType.TRUCK: Decimal("35")}

    def __init__(self):
        self.first_rates = dict(HourlyFee.RATES)
        self.EXTRA = dict(type(self).EXTRA)

    def calculate(self, kind, entered_at, exited_at):
        return self.first_rates[kind] + self.EXTRA[kind] * (billable_hours(entered_at, exited_at) - 1)
