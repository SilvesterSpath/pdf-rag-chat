from .pinecone import build_retriever
from functools import partial

retriever_map = {
  "pinecone_1": partial(build_retriever, k=1),
  "pinecone_2": partial(build_retriever, k=2),
  "pinecone_3": partial(build_retriever, k=3),
  "pinecone_4": partial(build_retriever, k=4),
}

retriever = retriever_map["pinecone_2"]
