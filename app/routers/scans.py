from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import ScanJobResponse
from app.models.scan_job import ScanJob
from app.models.project import Project
from app.workers.tasks import run_scan_task

router = APIRouter()

@router.post("/{project_id}", response_model=ScanJobResponse)
def start_scan(project_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Project not found")
    job = ScanJob(project_id=project.id, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    background_tasks.add_task(run_scan_task, job.id)
    return job

@router.get("/{scan_id}", response_model=ScanJobResponse)
def get_scan_status(scan_id: int, db: Session = Depends(get_db)):
    return db.query(ScanJob).filter(ScanJob.id == scan_id).first()