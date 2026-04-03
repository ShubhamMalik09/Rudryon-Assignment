from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.connection import get_db
from services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])

service = SensorService()

@router.get("")
def get_sensors(db: Session = Depends(get_db)):
    sensors = service.get_sensors(db)

    return [
        {
            "id": s.id,
            "name": s.name,
            "created_at": s.created_at
        }
        for s in sensors
    ]


@router.get("/{sensor_id}/readings")
def get_readings(sensor_id: int, db: Session = Depends(get_db)):
    readings = service.get_readings(db, sensor_id)

    return [
        {
            "id": r.id,
            "sensor_id": r.sensor_id,
            "temperature": r.temperature,
            "timestamp": r.timestamp,
            "is_anomaly": r.is_anomaly,
            "rolling_avg": r.rolling_avg
        }
        for r in readings
    ]


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = service.get_alerts(db)

    return [
        {
            "id": reading.id,
            "sensor_id": reading.sensor_id,
            "sensor_name": sensor_name,
            "temperature": reading.temperature,
            "timestamp": reading.timestamp,
            "is_anomaly": reading.is_anomaly,
            "rolling_avg": reading.rolling_avg
        }
        for reading, sensor_name in alerts
    ]
