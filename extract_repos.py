import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN environment variable not set.")
    print("Please, ensure that you have your GITHUB_TOKEN in a .env file in the project's root.")
    exit()

request_headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

api_url = "https://api.github.com/search/repositories"

search_params = {
    "q": "language:python",
    "sort": "forks",
    "order": "desc",
    "per_page": 50
}

response = requests.get(api_url, params=search_params, headers=request_headers)

if response.status_code == 200:
    repos_data = response.json()
    repositories = repos_data.get("items", [])
