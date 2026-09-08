from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.chat.vector_stores.pinecone import vectorstore


def _safe_print(text: str) -> None:
    """Print without flipping the console encoding (Flask watchdog reloads on that)."""
    print(text.encode("ascii", "replace").decode("ascii"), flush=True)


def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    """Load a PDF, split it into chunks, and upsert embeddings to Pinecone."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    loader = PyPDFLoader(pdf_path)
    docs = loader.load_and_split(text_splitter)

    for doc in docs:
        doc.metadata = {
            "page": doc.metadata["page"],
            "text": doc.page_content,
            "pdf_id": pdf_id,
        }

    _safe_print(f"{len(docs)} chunks from {pdf_id}")
    if docs:
        _safe_print(docs[0].page_content[:500])

    vectorstore.add_documents(docs)
    _safe_print(f"Upserted vectors: {len(docs)}")
