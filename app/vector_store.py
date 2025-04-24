# app/vector_store.py

import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from typing import List
from config import OPENAI_API_KEY, FAISS_INDEX_PATH

def create_vector_store(chunks: List[dict], persist_path: str = FAISS_INDEX_PATH) -> FAISS:
    """
    Embeds and stores text chunks in FAISS vector store.
    """
    docs = [
        Document(page_content=chunk["content"], metadata=chunk["metadata"])
        for chunk in chunks
    ]

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(persist_path)
    return vectorstore


def load_vector_store(persist_path: str = FAISS_INDEX_PATH) -> FAISS:
    index_path = os.path.join(persist_path, "index.faiss")
    if not os.path.exists(index_path):
        raise FileNotFoundError(
            f"Vector index not found at {index_path}. Run `pipeline_build_index.py` to generate it."
        )

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)

