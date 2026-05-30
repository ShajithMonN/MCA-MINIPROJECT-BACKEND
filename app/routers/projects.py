from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import ProjectCreate, ProjectResponse
from app.models.project import Project

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    # Dummy installation_id for now
    installation_id = "12345678"
    name = data.repo_url.rstrip("/").split("/")[-1]
    project = Project(
        name=name,
        github_url=data.repo_url,
        owner_id=1,
        installation_id=installation_id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()