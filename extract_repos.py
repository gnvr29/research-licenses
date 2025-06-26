import requests
import os
from dotenv import load_dotenv

def extract_repos_zip():

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

    output_directory = "files"
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    print("Attempting to fetch repositories from GitHub API...")
    response = requests.get(api_url, params=search_params, headers=request_headers)

    if response.status_code == 200:
        repos_data = response.json()
        repositories = repos_data.get("items", [])

        print(f"GitHub API returned {len(repositories)} repositories.")
        if not repositories:
            print("No repositories found for the search query. Nothing to download.")
            return

        for i, repo in enumerate(repositories):
            repo_full_name = repo["full_name"]
            default_branch = repo.get("default_branch", "main")

            download_url = f"https://github.com/{repo_full_name}/archive/refs/heads/{default_branch}.zip"
            file_name = f"{repo['owner']['login']}-{repo['name']}.zip"
            output_path = os.path.join(output_directory, file_name)

            print(f"[{i+1}/{len(repositories)}] Downloading '{repo_full_name}' from {download_url} to {output_path}...")

            try:
                download_response = requests.get(download_url, headers=request_headers, stream=True)
                download_response.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in download_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded: {file_name}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {repo_full_name}: {e}")
            except IOError as e:
                print(f"Error saving file {output_path}: {e}")
    else:
        print(f"Error fetching repositories. Status code: {response.status_code}")
        print(f"Full response from GitHub: {response.text}")

