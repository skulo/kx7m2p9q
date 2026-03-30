from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.measurement import Measurement
from app.models.sensor import Sensor
from app.schemas.measurement import MeasurementCreate, QueryParams, QueryResult


class MeasurementService:
    def __init__(self, db: Session):
        self.db = db

    def add_measurement(self, sensor_id: str, data: MeasurementCreate) -> Measurement:
        sensor = self.db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
        if not sensor:
            raise HTTPException(status_code=404, detail=f"Sensor '{sensor_id}' not found")

        measurement = Measurement(
            sensor_id=sensor_id,
            metric=data.metric,
            value=data.value,
            recorded_at=data.recorded_at or datetime.utcnow(),
        )
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement

    def query_measurements(self, params: QueryParams) -> list[QueryResult]:
        self._validate_date_range(params.date_from, params.date_to)

        date_from, date_to = self._resolve_date_range(params.date_from, params.date_to)

        query = self.db.query(
            Measurement.sensor_id,
            Measurement.metric,
            func.avg(Measurement.value).label("average"),
        ).filter(
            Measurement.metric.in_(params.metrics),
            Measurement.recorded_at >= date_from,
            Measurement.recorded_at <= date_to,
        )

        if params.sensor_ids:
            query = query.filter(Measurement.sensor_id.in_(params.sensor_ids))

        results = query.group_by(Measurement.sensor_id, Measurement.metric).all()

        if not results:
            raise HTTPException(status_code=404, detail="No measurements found for the given parameters")

        return [
            QueryResult(sensor_id=row.sensor_id, metric=row.metric, average=round(row.average, 2))
            for row in results
        ]

    def _validate_date_range(self, date_from: datetime | None, date_to: datetime | None) -> None:
        if date_from and date_to:
            if date_from > date_to:
                raise HTTPException(status_code=400, detail="date_from must be before date_to")
            if (date_to - date_from).days > 31:
                raise HTTPException(status_code=400, detail="Date range cannot exceed 31 days")

    def _resolve_date_range(self, date_from: datetime | None, date_to: datetime | None) -> tuple[datetime, datetime]:
        if not date_from and not date_to:
            date_to = datetime.utcnow()
            date_from = date_to - timedelta(days=1)
        elif not date_from:
            date_from = date_to - timedelta(days=1)
        elif not date_to:
            date_to = datetime.utcnow()
        return date_from, date_to
