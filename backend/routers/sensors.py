from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.connection import get_db
from services.sensor_service import SensorService
from schemas.sensor_schema import SensorOut, ReadingOut, AlertOut

router = APIRouter(prefix="/sensors", tags=["Sensors"])

service = SensorService()

@router.get("",response_model=List[SensorOut])
def get_sensors(db: Session = Depends(get_db)):
    return service.get_sensors(db)


@router.get("/{sensor_id}/readings", response_model=List[ReadingOut])
def get_readings(sensor_id: int, db: Session = Depends(get_db)):
    return service.get_readings(db, sensor_id, limit = 10, order = "desc")


@router.get("/alerts", response_model=List[AlertOut])
def get_alerts(db: Session = Depends(get_db)):
    alerts = service.get_alerts(db)

    return [
        AlertOut(
            id = reading.id,
            sensor_id =  reading.sensor_id,
            sensor_name = sensor_name,
            temperature = reading.temperature,
            timestamp = reading.timestamp,
            is_anomaly = reading.is_anomaly,
            rolling_avg = reading.rolling_avg
        )
        for reading, sensor_name in alerts
    ]
