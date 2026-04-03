import time
import random
from sqlalchemy import text

from db.connection import SessionLocal, engine
from models.sensor import Sensor, SensorReading


SENSORS = [
    {"id": 1, "name": "Sensor-Alpha"},
    {"id": 2, "name": "Sensor-Beta"},
    {"id": 3, "name": "Sensor-Gamma"},
]

def create_tables():
    Sensor.metadata.create_all(bind=engine)
    SensorReading.metadata.create_all(bind=engine)
    print("✅ Tables created!")

def seed_sensors():
    db = SessionLocal()

    try:
        for s in SENSORS:
            existing = db.execute(
                text("SELECT id FROM sensors WHERE id = :id"),
                {"id": s["id"]}
            ).fetchone()

            if not existing:
                sensor = Sensor(id=s["id"], name=s["name"])
                db.add(sensor)

        db.commit()
        print("✅ Sensors seeded!")

    finally:
        db.close()


def generate_temperature():
    if random.random() < 0.1:
        return round(random.uniform(85, 95), 2)
    return round(random.uniform(20, 85), 2)


def save_reading(sensor_id: int, temperature: float):
    db = SessionLocal()

    try:
        sql = text("""
            SELECT AVG(temperature) as avg_temp
            FROM sensor_readings
            WHERE sensor_id = :sensor_id
            AND timestamp >= NOW() - INTERVAL '1 hour'
        """)

        result = db.execute(sql, {"sensor_id": sensor_id})
        row = result.fetchone()

        rolling_avg = float(row[0]) if row[0] is not None else None

        is_anomaly = False
        if rolling_avg and temperature > rolling_avg * 1.15:
            is_anomaly = True

        reading = SensorReading(
            sensor_id=sensor_id,
            temperature=temperature,
            is_anomaly=is_anomaly,
            rolling_avg=rolling_avg
        )

        db.add(reading)
        db.commit()

        status = "🔴 ALERT" if temperature > 80 else ("🟡 WARN" if temperature > 70 else "🟢 OK")
        anomaly = " ⚠️ ANOMALY" if is_anomaly else ""
        avg_display = f"{rolling_avg:.2f}" if rolling_avg else "N/A"

        print(f"[{SENSORS[sensor_id-1]['name']}] {temperature}°C  {status}{anomaly}  (avg: {avg_display})")

    finally:
        db.close()


# ✅ Main loop (sync)
def run():
    create_tables()
    seed_sensors()

    print("🚀 Simulator running — pushing readings every 30 seconds...\n")

    while True:
        for sensor in SENSORS:
            temp = generate_temperature()
            save_reading(sensor["id"], temp)

        time.sleep(30)


if __name__ == "__main__":
    run()