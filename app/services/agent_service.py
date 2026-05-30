from app.agents.surgeon import SurgeonAgent

def generate_fix_for_finding(project_id: int, finding, file_content: str) -> str:
    surgeon = SurgeonAgent(project_id)
    return surgeon.generate_fix(finding, file_content)