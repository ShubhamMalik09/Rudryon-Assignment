from sqlalchemy.orm import Session
from models.sensor import Sensor, SensorReading

class SensorService:

    def get_sensors(self, db: Session):
        return db.query(Sensor).all()


    def get_readings(self, db: Session, sensor_id: int, limit : int = None, order: str = "desc"):
        order = order.lower()
        if order not in ["desc", "asc"]:
            order = "desc"
        
        query = db.query(SensorReading).filter(SensorReading.sensor_id == sensor_id)
        
        if order == "asc":
            query = query.order_by(SensorReading.timestamp.asc())
        else:
            query = query.order_by(SensorReading.timestamp.desc())
        
        if limit:
            query = query.limit(limit)
        
        readings = query.all()
        return readings


    def get_alerts(self, db: Session):
        results = (
            db.query(SensorReading, Sensor.name.label("sensor_name"))
            .join(Sensor, Sensor.id == SensorReading.sensor_id)
            .filter(SensorReading.temperature > 80)
            .order_by(SensorReading.timestamp.desc())
            .all()
        )

        return results