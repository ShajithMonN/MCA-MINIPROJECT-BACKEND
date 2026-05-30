import os, shutil
from git import Repo
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.config import settings
from app.services.embedding_service import LocalEmbeddings

class RAGService:
    def __init__(self):
        # Use local, free embeddings instead of OpenAI
        self.embeddings = LocalEmbeddings(model_name="all-MiniLM-L6-v2")
        self.persist_dir = settings.CHROMA_PERSIST_DIR

    def index_repository(self, repo_url: str, project_id: int):
        temp_dir = f"C:/temp/repo-{project_id}"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        Repo.clone_from(repo_url, temp_dir)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        docs = []
        for root, dirs, files in os.walk(temp_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules','venv','__pycache__']]
            for file in files:
                if file.endswith(('.py','.js','.ts','.jsx','.tsx')):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    except:
                        continue
                    chunks = text_splitter.split_text(content)
                    rel_path = path.replace(temp_dir, '')
                    for i, chunk in enumerate(chunks):
                        docs.append({
                            "text": chunk,
                            "metadata": {"source": rel_path, "chunk": i, "project_id": project_id}
                        })

        collection = f"project_{project_id}"
        Chroma.from_texts(
            texts=[d["text"] for d in docs],
            embedding=self.embeddings,   # local embeddings
            metadatas=[d["metadata"] for d in docs],
            persist_directory=os.path.join(self.persist_dir, collection),
            collection_name=collection
        )
        shutil.rmtree(temp_dir)
        return len(docs)

    def retrieve_context(self, project_id: int, query: str, k=4) -> str:
        collection = f"project_{project_id}"
        vectorstore = Chroma(
            persist_directory=os.path.join(self.persist_dir, collection),
            embedding_function=self.embeddings,   # local embeddings
            collection_name=collection
        )
        docs = vectorstore.similarity_search(query, k=k)
        parts = [f"// File: {d.metadata['source']}\n{d.page_content}" for d in docs]
        return "\n\n".join(parts)