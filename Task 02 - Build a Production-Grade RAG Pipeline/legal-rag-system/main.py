import os

from src.ingest import load_pdfs
from src.chunking import chunk_documents
from src.embedding import get_embedding_model
from src.vector_store import create_vector_store, save_vector_store, load_vector_store
from src.retriever import get_retriever
from src.generator import Generator
from dotenv import load_dotenv

load_dotenv()


class RAGPipeline:
    def __init__(self, db):
        self.db = db
        self.retriever = get_retriever(db)
        self.generator = Generator()

    def query(self, question):
        docs = self.retriever.invoke(question)

        answer = self.generator.generate(question, docs)

        sources = []
        for doc in docs:
            sources.append({
                "document": doc.metadata.get("document"),
                "page": doc.metadata.get("page"),
                "chunk": doc.page_content[:200]
            })

        confidence = min(1.0, len(docs) / 3)

        if not docs:
            answer = "Not enough information"
            confidence = 0.0

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }


if __name__ == "__main__":

    pdf_files = []
    for file in os.listdir("data/contracts/"):
        if file.endswith(".pdf"):
            pdf_files.append(f"data/contracts/{file}")
    
    if len(pdf_files) < 1:
        print("[+] No Contracts found.")
        raise SystemExit

    docs = load_pdfs(pdf_files)
    chunks = chunk_documents(docs)

    embed_model = get_embedding_model()
    db = create_vector_store(chunks, embed_model)

    save_vector_store(db, "./faiss_index")

    pipeline = RAGPipeline(db)

    result = pipeline.query(
        "Which is the best model to predict the blood group?"
    )

    print(result)