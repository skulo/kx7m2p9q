from datetime import datetime
from pydantic import BaseModel, field_validator


class MeasurementCreate(BaseModel):
    metric: str
    value: float
    recorded_at: datetime | None = None


class MeasurementResponse(BaseModel):
    id: int
    sensor_id: str
    metric: str
    value: float
    recorded_at: datetime

    model_config = {"from_attributes": True}


class QueryParams(BaseModel):
    sensor_ids: list[str] | None = None
    metrics: list[str]
    date_from: datetime | None = None
    date_to: datetime | None = None

    @field_validator("metrics")
    @classmethod
    def metrics_not_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("At least one metric must be specified")
        return v


class QueryResult(BaseModel):
    sensor_id: str
    metric: str
    average: float
