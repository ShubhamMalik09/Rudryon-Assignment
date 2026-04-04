from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.connection import engine
from models.sensor import Base
from routers import sensors, websocket
import asyncio
from utils.background_simulator import run_simulator
from utils.seed_sensor import seed_sensors_if_empty
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting app...")

    # Create tables
    Base.metadata.create_all(bind=engine)

    # seed sensors if not exists in db
    seed_sensors_if_empty()

    # Start background simulator
    task = asyncio.create_task(run_simulator())

    yield   # app runs here

    print("🛑 Shutting down...")
    task.cancel()

app = FastAPI(title="Sensor Monitoring API", version="1.0.0", lifespan=lifespan)

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