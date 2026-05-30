from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from app.services.rag_service import RAGService
from app.config import settings

class AuditorAgent:
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.llm = ChatOpenAI(
            model="deepseek-chat",                # DeepSeek model
            temperature=0,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL   # DeepSeek endpoint
        )
        self.rag = RAGService()

    def search_codebase(self, query: str) -> str:
        return self.rag.retrieve_context(self.project_id, query)

    def analyze_file(self, file_path: str, file_content: str) -> str:
        tools = [
            Tool(name="search_codebase", func=self.search_codebase,
                 description="Search the codebase for relevant code using semantic similarity.")
        ]
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a security auditor. Analyze the code and output valid JSON with key 'findings' (array).
Each object: file, line, severity, cwe_id, description, suggested_fix_type.
Use search_codebase to get context. If no issues, empty array."""),
            ("user", f"File: {file_path}\nContent:\n{file_content}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        result = executor.invoke({"input": "Analyze this file."})
        return result["output"]