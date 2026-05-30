from langchain_openai import ChatOpenAI
from app.services.rag_service import RAGService
from app.config import settings

class SurgeonAgent:
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            temperature=0,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )
        self.rag = RAGService()

    def generate_fix(self, finding, file_content: str) -> str:
        context = self.rag.retrieve_context(self.project_id,
            f"{finding.description} around line {finding.line_number}")
        prompt = f"""Fix the following security issue in the code.
Vulnerability: {finding.description}
CWE: {finding.cwe_id}
File: {finding.file_path}
Line: {finding.line_number}

Relevant code context from the project (use these imports/functions):
{context}

Current code snippet (the whole file):
{file_content}

Generate the corrected code for the entire file. Only output the fixed code, nothing else."""
        response = self.llm.invoke(prompt)
        return response.content