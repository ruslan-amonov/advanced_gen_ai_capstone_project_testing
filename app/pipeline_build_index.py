import os
from document_loader import load_all_pdfs
from vector_store import create_vector_store


# Always resolve from project root
data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
data_folder = os.path.abspath(data_folder)

chunks = load_all_pdfs(data_folder)
print(f"Loaded {len(chunks)} chunks.")
print(chunks[0])


vectorstore = create_vector_store(chunks)
print("Vector store created and saved.")


print("Saving FAISS index to:", os.path.abspath("faiss_index"))
vectorstore = create_vector_store(chunks)
