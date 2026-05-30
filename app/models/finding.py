from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True)
    scan_job_id = Column(Integer, ForeignKey("scan_jobs.id"))
    file_path = Column(Text, nullable=False)
    line_number = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    cwe_id = Column(String)
    description = Column(Text, nullable=False)
    fixed_code_suggestion = Column(Text)
    status = Column(String, default="open")