from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database
import requests

router = APIRouter(
    prefix="/environments",
    tags=["environments"]
)


@router.post("/", response_model=schemas.Environment)
def create_environment(environment: schemas.EnvironmentCreate, db: Session = Depends(database.get_db)):
    db_env = models.Environment(name=environment.name, config=environment.config)
    db.add(db_env)
    db.commit()
    db.refresh(db_env)
    return db_env


@router.get("/{environment_id}", response_model=schemas.Environment)
def read_environment(environment_id: int, db: Session = Depends(database.get_db)):
    db_env = db.query(models.Environment).filter(models.Environment.id == environment_id).first()
    if db_env is None:
        raise HTTPException(status_code=404, detail="Environment not found")
    return db_env


@router.post("/{environment_id}/run")
def run_environment(environment_id: int, db: Session = Depends(database.get_db)):
    db_env = db.query(models.Environment).filter(models.Environment.id == environment_id).first()
    if db_env is None:
        raise HTTPException(status_code=404, detail="Environment not found")

    response = requests.post("http://second_service:8001/run", json={"name": db_env.name, "config": db_env.config})

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to run environment")

    return {"message": "Environment is running"}
