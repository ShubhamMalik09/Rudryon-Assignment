import random
import asyncio
from sqlalchemy import text

from db.connection import SessionLocal
from models.sensor import SensorReading


def generate_temperature():
    if random.random() < 0.1:
        return round(random.uniform(85, 95), 2)
    return round(random.uniform(20, 85), 2)


async def run_simulator():
    print("🚀 Sensor simulator started...")

    while True:
        db = SessionLocal()

        try:

            # currently assuming there are only these 3 ids
            for sensor_id in [1, 2, 3]:
                temp = generate_temperature()

                result = db.execute(text("""
                    SELECT AVG(temperature)
                    FROM sensor_readings
                    WHERE sensor_id = :sensor_id
                    AND timestamp >= NOW() - INTERVAL '1 hour'
                """), {"sensor_id": sensor_id})

                row = result.fetchone()
                rolling_avg = float(row[0]) if row[0] else None

                is_anomaly = False
                if rolling_avg and temp > rolling_avg * 1.15:
                    is_anomaly = True

                reading = SensorReading(
                    sensor_id=sensor_id,
                    temperature=temp,
                    is_anomaly=is_anomaly,
                    rolling_avg=rolling_avg
                )

                db.add(reading)

            db.commit()

        finally:
            db.close()

        await asyncio.sleep(random.randint(20, 30))