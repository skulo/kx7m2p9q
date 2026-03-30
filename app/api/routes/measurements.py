from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.measurement import MeasurementCreate, MeasurementResponse, QueryParams, QueryResult
from app.services.measurement_service import MeasurementService

router = APIRouter(tags=["measurements"])

@router.post("/sensors/{sensor_id}/measurements", response_model=MeasurementResponse)
def add_measurement(sensor_id: str, data: MeasurementCreate, db: Session = Depends(get_db)):
    service = MeasurementService(db)
    return service.add_measurement(sensor_id, data)

@router.get("/measurements/query", response_model=list[QueryResult])
def query_measurements(
    metrics: list[str] = Query(..., description="Metrics to include, e.g. temperature"),
    sensor_ids: list[str] | None = Query(None, description="One or more sensor IDs"),
    date_from: str | None = Query(None, description="ISO format date"),
    date_to: str | None = Query(None, description="ISO format date"),
    db: Session = Depends(get_db)
):
    params = QueryParams(
        sensor_ids=sensor_ids,
        metrics=metrics,
        date_from=date_from,
        date_to=date_to
    )
    service = MeasurementService(db)
    return service.query_measurements(params)
