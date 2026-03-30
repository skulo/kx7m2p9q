from fastapi import FastAPI
from app.api.routes import sensors, measurements

app = FastAPI(title="Weather Sensor API")

app.include_router(sensors.router)
app.include_router(measurements.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
