"""Replaceable allocation and fee rules. Amounts are illustrative INR rates."""
from abc import ABC, abstractmethod
from decimal import Decimal
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
    seconds = (exited_at - entered_at).total_seconds()
    if seconds < 0:
        raise ValueError("Exit time precedes entry")
    return max(1, ceil(seconds / 3600))


class HourlyFee(FeeStrategy):
    RATES = {VehicleType.BIKE: Decimal("10"), VehicleType.CAR: Decimal("20"), VehicleType.TRUCK: Decimal("50")}

    def calculate(self, kind, entered_at, exited_at):
        return self.RATES[kind] * billable_hours(entered_at, exited_at)


class TieredFee(FeeStrategy):
    EXTRA = {VehicleType.BIKE: Decimal("5"), VehicleType.CAR: Decimal("15"), VehicleType.TRUCK: Decimal("35")}

    def calculate(self, kind, entered_at, exited_at):
        return HourlyFee.RATES[kind] + self.EXTRA[kind] * (billable_hours(entered_at, exited_at) - 1)
