from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate


class SensorService:
    def __init__(self, db: Session):
        self.db = db

    def create_sensor(self, data: SensorCreate) -> Sensor:
        existing = self.db.query(Sensor).filter(Sensor.sensor_id == data.sensor_id).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Sensor '{data.sensor_id}' already exists")

        sensor = Sensor(
            sensor_id=data.sensor_id,
            country=data.country,
            city=data.city,
        )
        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)
        return sensor

    def get_all_sensors(self) -> list[Sensor]:
        return self.db.query(Sensor).all()

    def get_sensor_by_id(self, sensor_id: str) -> Sensor:
        sensor = self.db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
        if not sensor:
            raise HTTPException(status_code=404, detail=f"Sensor '{sensor_id}' not found")
        return sensor
