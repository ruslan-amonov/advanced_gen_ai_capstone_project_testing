# config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Company metadata
COMPANY_INFO = {
    "name": "birth of EngInE [моторчик]",
    "email": "ruslan.amonov@yahoo.com",
    "phone": "+998 33 964 7181",
}

# Global FAISS vector path
FAISS_INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "faiss_index"))

GITHUB = {
    "repo_owner": "ruslan-amonov",
    "repo_name": "advanced_gen_ai_capstone_project_testing"
}

