from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import FindingResponse
from app.models.finding import Finding

router = APIRouter()

@router.get("/{scan_job_id}", response_model=list[FindingResponse])
def list_findings(scan_job_id: int, db: Session = Depends(get_db)):
    return db.query(Finding).filter(Finding.scan_job_id == scan_job_id).all()

@router.post("/{finding_id}/fix")
def generate_fix(finding_id: int, db: Session = Depends(get_db)):
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Finding not found")
    # Placeholder fix
    finding.fixed_code_suggestion = "# Fixed code placeholder"
    finding.status = "fix_generated"
    db.commit()
    return {"status": "fix generated", "preview": finding.fixed_code_suggestion}