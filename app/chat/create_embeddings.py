import sys

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    """Load a PDF, split it into chunks, and print a sample (embeddings next)."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    loader = PyPDFLoader(pdf_path)
    docs = loader.load_and_split(text_splitter)

    # Windows consoles often use cp1250 and crash on PDF text like "ã"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"{len(docs)} chunks from {pdf_id}", flush=True)
    if docs:
        print(docs[0].page_content[:500], flush=True)
