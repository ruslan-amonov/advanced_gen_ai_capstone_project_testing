# utils/github_issues.py

import requests
from config import GITHUB_TOKEN, GITHUB

def create_github_issue(name, email, summary, description):
    repo_owner = GITHUB["repo_owner"]
    repo_name = GITHUB["repo_name"]
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "title": f"[Support] {summary}",
        "body": f"**From**: {name} ({email})\n\n**Issue**:\n{description}",
        "labels": ["support", "streamlit"]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return True
    else:
        print("❌ GitHub API Error:", response.status_code, response.text)
        return False

