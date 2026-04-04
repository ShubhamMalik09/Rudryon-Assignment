from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.connection import engine
from models.sensor import Base
from routers import sensors, websocket


app = FastAPI(title="Sensor Monitoring API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router)
app.include_router(websocket.router)


@app.get("/")
def root():
    return {"message": "API is running 🚀"}