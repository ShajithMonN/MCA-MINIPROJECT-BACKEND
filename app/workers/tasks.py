from app.database import SessionLocal
from app.models.scan_job import ScanJob
from app.models.project import Project
from app.services.scan_service import ScanService

def run_scan_task(scan_job_id: int):
    db = SessionLocal()
    try:
        job = db.query(ScanJob).filter(ScanJob.id == scan_job_id).first()
        if not job:
            return
        project = db.query(Project).filter(Project.id == job.project_id).first()
        job.status = "running"
        db.commit()

        service = ScanService()
        findings = service.scan_repository(project.id, scan_job_id, project.github_url)

        job.status = "completed"
        job.summary = {"total_findings": len(findings)}
        db.commit()
    except Exception as e:
        job.status = "failed"
        job.summary = {"error": str(e)}
        db.commit()
    finally:
        db.close()