import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from parking_lot import ParkingLot, TieredFee, HighestFloor
from parking_lot.strategies import FeeStrategy, HourlyFee, billable_hours
from parking_lot.models import VehicleType, ParkingSlot
from zoneinfo import ZoneInfo


class ParkingTests(unittest.TestCase):
    def setUp(self):
        self.start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.lot = ParkingLot("Test", clock=lambda: self.start)
        for floor in (1, 2):
            self.lot.add_floor(floor)
            for kind in ("BIKE", "CAR", "TRUCK"):
                self.lot.add_slot(floor, kind, kind)

    def test_allocation_and_reuse(self):
        a = self.lot.park("a", "CAR")
        b = self.lot.park("b", "CAR")
        self.assertEqual((a.floor, b.floor), (1, 2))
        with self.assertRaises(ValueError):
            self.lot.park("c", "CAR")
        self.lot.unpark(a.ticket_id)
        self.assertEqual(self.lot.park("c", "CAR").floor, 1)

    def test_duplicate_plate_normalized(self):
        self.lot.park(" ab-123 ", "bike")
        with self.assertRaises(ValueError):
            self.lot.park("AB-123", "CAR")

    def test_wrong_type_cannot_take_free_car_slot(self):
        self.lot.park("a", "BIKE")
        self.lot.park("b", "BIKE")
        with self.assertRaises(ValueError):
            self.lot.park("c", "BIKE")
        self.assertEqual(len(self.lot.free_slots("CAR")), 2)

    def test_fee_rounding(self):
        for seconds, expected in [(0, 20), (3599, 20), (3600, 20), (3601, 40), (10800, 60)]:
            t = self.lot.park("a", "CAR")
            receipt = self.lot.unpark(t.ticket_id, self.start + timedelta(seconds=seconds))
            self.assertEqual(receipt.fee, Decimal(expected))
            self.assertFalse(receipt.active)

    def test_tiered_and_pricing_snapshot(self):
        old = self.lot.park("a", "CAR")
        self.lot.set_strategies(pricing=TieredFee())
        new = self.lot.park("b", "CAR")
        end = self.start + timedelta(hours=4)
        self.assertEqual(self.lot.unpark(old.ticket_id, end).fee, Decimal(80))
        self.assertEqual(self.lot.unpark(new.ticket_id, end).fee, Decimal(65))

    def test_failed_exit_preserves_state(self):
        t = self.lot.park("a", "CAR")
        before = self.lot.occupancy()
        with self.assertRaises(ValueError):
            self.lot.unpark(t.ticket_id, self.start - timedelta(seconds=1))
        self.assertEqual(self.lot.occupancy(), before)
        with self.assertRaises(ValueError):
            self.lot.park("a", "CAR")
        self.assertEqual(self.lot.unpark(t.ticket_id).fee, Decimal(20))

    def test_failed_fee_preserves_state(self):
        class BrokenFee(FeeStrategy):
            calls = 0
            def calculate(self, *args):
                self.calls += 1
                if self.calls == 1:
                    raise ValueError("pricing unavailable")
                return Decimal(20)
        self.lot.set_strategies(pricing=BrokenFee())
        t = self.lot.park("a", "CAR")
        before = self.lot.occupancy()
        with self.assertRaises(ValueError):
            self.lot.unpark(t.ticket_id)
        self.assertEqual(self.lot.occupancy(), before)

        with self.assertRaises(ValueError):
            self.lot.park("a", "CAR")
        self.assertEqual(self.lot.unpark(t.ticket_id).fee, Decimal(20))
        self.assertTrue(self.lot.park("a", "CAR").active)

    def test_dst_elapsed_time_and_order(self):
        zone = ZoneInfo("America/New_York")
        start = datetime(2026, 11, 1, 1, 45, tzinfo=zone, fold=0)
        end = datetime(2026, 11, 1, 1, 15, tzinfo=zone, fold=1)
        t = self.lot.park("dst", "CAR", start)
        self.assertEqual(self.lot.unpark(t.ticket_id, end).fee, Decimal(20))
        self.assertEqual(billable_hours(datetime(2026, 11, 1, 0, 30, tzinfo=zone),
                                       datetime(2026, 11, 1, 2, 30, tzinfo=zone)), 3)
        self.assertEqual(billable_hours(datetime(2026, 3, 8, 1, 30, tzinfo=zone),
                                       datetime(2026, 3, 8, 3, 30, tzinfo=zone)), 1)

    def test_mutable_pricing_is_snapshotted(self):
        pricing = HourlyFee()
        self.lot.set_strategies(pricing=pricing)
        old = self.lot.park("old", "CAR")
        pricing.RATES[VehicleType.CAR] = Decimal(99)
        new = self.lot.park("new", "CAR")
        self.assertEqual(self.lot.unpark(old.ticket_id).fee, Decimal(20))
        self.assertEqual(self.lot.unpark(new.ticket_id).fee, Decimal(99))

    def test_invalid_allocator_cannot_corrupt_state(self):
        class BadAllocator:
            def choose(self, available):
                return ParkingSlot(1, "CAR", VehicleType.CAR)
        old = self.lot.park("old", "CAR")
        before = self.lot.occupancy()
        self.lot.set_strategies(allocation=BadAllocator())
        with self.assertRaises(ValueError):
            self.lot.park("new", "CAR")
        self.assertEqual(self.lot.occupancy(), before)
        self.assertEqual(self.lot.unpark(old.ticket_id).fee, Decimal(20))

    def test_falsey_strategies_and_boolean_floor(self):
        class FalseHigh(HighestFloor):
            def __bool__(self): return False
        class FalseFee(HourlyFee):
            def __bool__(self): return False
            def calculate(self, *args): return Decimal(7)
        lot = ParkingLot("Falsey", allocation=FalseHigh(), pricing=FalseFee(), clock=lambda: self.start)
        with self.assertRaises(ValueError): lot.add_floor(True)
        for floor in (1, 2):
            lot.add_floor(floor)
            lot.add_slot(floor, "C", "CAR")
        t = lot.park("a", "CAR")
        self.assertEqual(t.floor, 2)
        self.assertEqual(lot.unpark(t.ticket_id).fee, Decimal(7))

    def test_unknown_and_closed_ticket(self):
        with self.assertRaises(ValueError):
            self.lot.unpark("unknown")
        t = self.lot.park("a", "TRUCK")
        self.lot.unpark(t.ticket_id)
        with self.assertRaises(ValueError):
            self.lot.unpark(t.ticket_id)

    def test_invalid_setup_and_vehicle(self):
        for action in [lambda: self.lot.add_floor(0), lambda: self.lot.add_floor(1),
                       lambda: self.lot.add_slot(9, "x", "CAR"), lambda: self.lot.add_slot(1, "CAR", "CAR"),
                       lambda: self.lot.add_slot(1, "", "CAR"), lambda: self.lot.park("", "CAR"),
                       lambda: self.lot.park("a", "PLANE"), lambda: self.lot.park("a", "CAR", datetime(2026, 1, 1))]:
            with self.assertRaises(ValueError):
                action()

    def test_strategy_and_safe_views(self):
        self.lot.set_strategies(allocation=HighestFloor())
        self.assertEqual(self.lot.park("a", "CAR").floor, 2)
        copy = self.lot.free_slots("CAR")[0]
        copy.ticket_id = "not-real"
        self.assertEqual(len(self.lot.free_slots("CAR")), 1)

    def test_concurrent_capacity(self):
        def attempt(i):
            try:
                return self.lot.park(str(i), "CAR")
            except ValueError:
                return None
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(attempt, range(20)))
        tickets = [t for t in results if t is not None]
        self.assertEqual(len(tickets), 2)
        self.assertEqual(len({(t.floor, t.slot_id) for t in tickets}), 2)


if __name__ == "__main__":
    unittest.main()
