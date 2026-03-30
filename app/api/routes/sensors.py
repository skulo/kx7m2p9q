from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.sensor import SensorCreate, SensorResponse
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.post("", response_model=SensorResponse)
def register_sensor(data: SensorCreate, db: Session = Depends(get_db)):
    service = SensorService(db)
    return service.create_sensor(data)

@router.get("", response_model=list[SensorResponse])
def list_sensors(db: Session = Depends(get_db)):
    service = SensorService(db)
    return service.get_all_sensors()
