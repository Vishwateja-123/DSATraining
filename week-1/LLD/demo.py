"""Run from any directory: python3 path/to/LLD/demo.py"""
from datetime import datetime, timedelta, timezone
from parking_lot import ParkingLot, TieredFee


def main():
    start = datetime(2026, 10, 26, 9, tzinfo=timezone.utc)
    lot = ParkingLot("Campus parking")
    for floor in (1, 2):
        lot.add_floor(floor)
    for floor, slot, kind in [(1, "B1", "BIKE"), (1, "C1", "CAR"), (2, "C1", "CAR"), (2, "T1", "TRUCK")]:
        lot.add_slot(floor, slot, kind)
    bike = lot.park("DEMO-BIKE", "BIKE", start)
    car = lot.park("DEMO-CAR", "CAR", start)
    truck = lot.park("DEMO-TRUCK", "TRUCK", start)
    print("Allocated floors:", bike.floor, car.floor, truck.floor)
    print("Car fee for 3 hours: INR", lot.unpark(car.ticket_id, start + timedelta(hours=3)).fee)
    lot.set_strategies(pricing=TieredFee())
    new_car = lot.park("DEMO-CAR-2", "CAR", start)
    print("Tiered car fee for 4 hours: INR", lot.unpark(new_car.ticket_id, start + timedelta(hours=4)).fee)
    for label, action in [
        ("Duplicate vehicle", lambda: lot.park("DEMO-BIKE", "BIKE", start)),
        ("Full truck slots", lambda: lot.park("TRUCK-2", "TRUCK", start)),
        ("Invalid ticket", lambda: lot.unpark("missing", start)),
        ("Repeated exit", lambda: lot.unpark(car.ticket_id, start)),
        ("Invalid vehicle type", lambda: lot.park("PLANE", "PLANE", start)),
        ("Duplicate floor", lambda: lot.add_floor(1)),
    ]:
        try:
            action()
        except ValueError:
            print(label + ": rejected")
    print("Occupancy:", lot.occupancy())


if __name__ == "__main__":
    main()
