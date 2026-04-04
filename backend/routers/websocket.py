import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from db.connection import SessionLocal
from services.sensor_service import SensorService
from schemas.sensor_schema import ReadingOut, AlertOut

router = APIRouter()
service = SensorService()

# @router.websocket("/ws/sensors")
# async def ws_sensors(websocket: WebSocket):
#     await websocket.accept()
#     print("✅ Sensors WS connected")

#     try:
#         while True:
#             db = SessionLocal()
#             try:
#                 sensors = service.get_sensors(db)

#                 data = [
#                     {
#                         "id": s.id,
#                         "name": s.name,
#                         "created_at": str(s.created_at)
#                     }
#                     for s in sensors
#                 ]

#                 await websocket.send_json(data)

#             finally:
#                 db.close()

#             await asyncio.sleep(30)

#     except WebSocketDisconnect:
#         print("❌ Sensors WS disconnected")


@router.websocket("/ws/sensors/{sensor_id}/readings")
async def ws_readings(websocket: WebSocket, sensor_id: int):
    await websocket.accept()
    print(f"✅ Readings WS connected for sensor {sensor_id}")

    try:
        while True:
            db = SessionLocal()
            try:
                readings = service.get_readings(db, sensor_id)

                data = [
                    ReadingOut.model_validate(r).model_dump()
                    for r in readings
                ]

                await websocket.send_json(data)

            finally:
                db.close()

            await asyncio.sleep(30)

    except WebSocketDisconnect:
        print(f"❌ Readings WS disconnected for sensor {sensor_id}")

@router.websocket("/ws/sensors/alerts")
async def ws_alerts(websocket: WebSocket):
    await websocket.accept()
    print("✅ Alerts WS connected")

    try:
        while True:
            db = SessionLocal()
            try:
                alerts = service.get_alerts(db)

                data = [
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

                await websocket.send_json(data)

            finally:
                db.close()

            await asyncio.sleep(30)

    except WebSocketDisconnect:
        print("❌ Alerts WS disconnected")