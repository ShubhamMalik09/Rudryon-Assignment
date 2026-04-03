from sqlalchemy.orm import Session
from models.sensor import Sensor, SensorReading

class SensorService:

    def get_sensors(self, db: Session):
        return db.query(Sensor).all()


    def get_readings(self, db: Session, sensor_id: int):
        readings = (
            db.query(SensorReading)
            .filter(SensorReading.sensor_id == sensor_id)
            .order_by(SensorReading.timestamp.desc())
            .all()
        )

        return readings


    def get_alerts(self, db: Session):
        results = (
            db.query(SensorReading, Sensor.name.label("sensor_name"))
            .join(Sensor, Sensor.id == SensorReading.sensor_id)
            .filter(SensorReading.temperature > 80)
            .order_by(SensorReading.timestamp.desc())
            .all()
        )

        alerts = []
        for reading, sensor_name in results:
            alerts.append({
                "id": reading.id,
                "sensor_id": reading.sensor_id,
                "sensor_name": sensor_name,
                "temperature": reading.temperature,
                "timestamp": reading.timestamp,
                "is_anomaly": reading.is_anomaly,
                "rolling_avg": reading.rolling_avg
            })

        return alerts