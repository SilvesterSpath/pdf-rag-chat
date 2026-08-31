import os
from langchain.vectorstores import Pinecone
from app.chat.embeddings.openai import embeddings

# pinecone-client 3.x removed pinecone.init(). LangChain's from_existing_index
# creates Pinecone(api_key=...) itself when the SDK is v3+.
vectorstore = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"),
    embeddings,
)
