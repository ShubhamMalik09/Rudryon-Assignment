import asyncio
import random
from db.connection import SessionLocal, engine
from models.sensor import Sensor, SensorReading
from sqlalchemy import text

# 3 Sensors data
SENSORS = [
    {"id": 1, "name": "Sensor-Alpha"},
    {"id": 2, "name": "Sensor-Beta"},
    {"id": 3, "name": "Sensor-Gamma"},
]

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Sensor.metadata.create_all)
        await conn.run_sync(SensorReading.metadata.create_all)
    print("✅ Tables created!")

async def seed_sensors():
    async with SessionLocal() as db:
        for s in SENSORS:
            result = await db.execute(
                text("SELECT id FROM sensors WHERE id = :id"),
                {"id": s["id"]}
            )
            existing = result.fetchone()
            if not existing:
                sensor = Sensor(id=s["id"], name=s["name"])
                db.add(sensor)
        await db.commit()
        print("✅ Sensors seeded!")

def generate_temperature():
    # 10% chance of spike to test anomaly
    if random.random() < 0.1:
        return round(random.uniform(85, 95), 2)
    return round(random.uniform(20, 85), 2)

async def save_reading(sensor_id: int, temperature: float):
    async with SessionLocal() as db:
        # Get 1 hour rolling average
        sql = text("""
            SELECT AVG(temperature) as avg_temp
            FROM sensor_readings
            WHERE sensor_id = :sensor_id
            AND timestamp >= NOW() - INTERVAL '1 hour'
        """)
        result = await db.execute(sql, {"sensor_id": sensor_id})
        row = result.fetchone()
        rolling_avg = float(row[0]) if row[0] is not None else None

        # Flag anomaly if 15% above rolling average
        is_anomaly = False
        if rolling_avg is not None and temperature > rolling_avg * 1.15:
            is_anomaly = True

        reading = SensorReading(
            sensor_id=sensor_id,
            temperature=temperature,
            is_anomaly=is_anomaly,
            rolling_avg=rolling_avg
        )
        db.add(reading)
        await db.commit()

        # Log output
        status = "🔴 ALERT" if temperature > 80 else ("🟡 WARN" if temperature > 70 else "🟢 OK")
        anomaly = " ⚠️  ANOMALY" if is_anomaly else ""
        avg_display = f"{rolling_avg:.2f}" if rolling_avg else "N/A"
        print(f"[{SENSORS[sensor_id-1]['name']}] {temperature}°C  {status}{anomaly}  (rolling avg: {avg_display}°C)")

async def run():
    await create_tables()
    await seed_sensors()

    print("🚀 Simulator running — pushing readings every 30 seconds...\n")

    while True:
        for sensor in SENSORS:
            temp = generate_temperature()
            await save_reading(sensor["id"], temp)
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(run())