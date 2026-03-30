from datetime import datetime
from pydantic import BaseModel


class SensorCreate(BaseModel):
    sensor_id: str
    country: str | None = None
    city: str | None = None


class SensorResponse(BaseModel):
    id: int
    sensor_id: str
    country: str | None
    city: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
