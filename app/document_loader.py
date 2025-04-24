# app/document_loader.py

import fitz  # PyMuPDF
import os
from typing import List, Dict


def load_pdf_with_pages(file_path: str) -> List[Dict]:
    """
    Loads a PDF and returns a list of chunks with metadata (source file and page number).
    """
    doc = fitz.open(file_path)
    chunks = []

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text()

        if text.strip():  # Skip empty pages
            chunks.append({
                "content": text.strip(),
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": page_number + 1  # 1-based index for users
                }
            })

    return chunks


def load_all_pdfs(folder_path: str) -> List[Dict]:
    """
    Loads and processes all PDF files in the given folder.
    """
    all_chunks = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            chunks = load_pdf_with_pages(file_path)
            all_chunks.extend(chunks)

    return all_chunks