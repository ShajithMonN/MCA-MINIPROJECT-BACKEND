import os, shutil, json
from git import Repo
from app.services.rag_service import RAGService
from app.agents.auditor import AuditorAgent
from app.database import SessionLocal
from app.models.finding import Finding

class ScanService:
    def scan_repository(self, project_id: int, scan_job_id: int, repo_url: str):
        # Index repository
        rag = RAGService()
        rag.index_repository(repo_url, project_id)

        # Clone for file analysis
        temp_dir = f"C:/temp/scan-{project_id}"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        Repo.clone_from(repo_url, temp_dir)

        auditor = AuditorAgent(project_id)
        db = SessionLocal()
        findings_list = []

        for root, dirs, files in os.walk(temp_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules','venv','__pycache__']]
            for file in files:
                if file.endswith(('.py','.js','.ts')):
                    path = os.path.join(root, file)
                    rel_path = path.replace(temp_dir, '')
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    try:
                        result = auditor.analyze_file(rel_path, content)
                        data = json.loads(result)
                    except:
                        continue
                    for find in data.get("findings", []):
                        finding = Finding(
                            scan_job_id=scan_job_id,
                            file_path=find["file"],
                            line_number=find["line"],
                            severity=find["severity"],
                            cwe_id=find.get("cwe_id"),
                            description=find["description"],
                            status="open"
                        )
                        db.add(finding)
                        findings_list.append(finding)
        db.commit()
        db.close()
        shutil.rmtree(temp_dir)
        return findings_list