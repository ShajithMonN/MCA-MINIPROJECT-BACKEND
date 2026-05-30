from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    repo_url: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    github_url: str
    owner_id: int
    installation_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ScanJobResponse(BaseModel):
    id: int
    project_id: int
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    summary: Optional[dict] = None
    class Config:
        from_attributes = True

class FindingResponse(BaseModel):
    id: int
    scan_job_id: int
    file_path: str
    line_number: int
    severity: str
    cwe_id: Optional[str] = None
    description: str
    fixed_code_suggestion: Optional[str] = None
    status: str
    class Config:
        from_attributes = True

class PullRequestResponse(BaseModel):
    id: int
    finding_id: int
    github_pr_number: str
    branch_name: str
    status: str
    created_at: datetime
    merged_at: Optional[datetime] = None
    class Config:
        from_attributes = True