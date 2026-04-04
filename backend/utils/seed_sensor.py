from db.connection import SessionLocal
from models.sensor import Sensor

DEFAULT_SENSORS = [
    {"id": 1, "name": "Sensor-Alpha"},
    {"id": 2, "name": "Sensor-Beta"},
    {"id": 3, "name": "Sensor-Gamma"},
]


def seed_sensors_if_empty():
    db = SessionLocal()

    try:
        count = db.query(Sensor).count()

        if count == 0:
            print("🌱 Seeding sensors...")

            sensors = [
                Sensor(
                    id=s["id"],
                    name=s["name"],
                )
                for s in DEFAULT_SENSORS
            ]

            db.add_all(sensors)
            db.commit()

            print("✅ Sensors seeded!")

        else:
            print("ℹ️ Sensors already exist")

    finally:
        db.close()