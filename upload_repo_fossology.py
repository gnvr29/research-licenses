import os
import time
import requests
import sys
from dotenv import load_dotenv

FOSSOLOGY_URL = "http://localhost:8081"

load_dotenv()

API_TOKEN = os.getenv("FOSSOLOGY_TOKEN")

def upload_all_zips_in_directory(directory_path):
    """
    Finds all .zip files in a given directory and uploads them sequentially to FOSSology.

    Args:
        directory_path (str): The path to the directory containing .zip files.
    """
    print("--- Starting FOSSology Batch Upload ---")

    # Basic check to ensure the user has updated the placeholder token.
    if "YOUR_API_TOKEN_HERE" in API_TOKEN:
        print("\nERROR: Please edit the script and replace 'YOUR_API_TOKEN_HERE' with your actual API token.")
        sys.exit(1)

    # Check if the target directory exists.
    if not os.path.isdir(directory_path):
        print(f"\nERROR: Directory '{directory_path}' not found.")
        print("Please create it and place your .zip files inside.")
        sys.exit(1)

    # Find all files in the directory that end with .zip
    zip_files_to_upload = [f for f in os.listdir(directory_path) if f.lower().endswith('.zip')]

    if not zip_files_to_upload:
        print(f"\nNo .zip files found in the '{directory_path}' directory. Nothing to do.")
        return

    print(f"Found {len(zip_files_to_upload)} .zip file(s) to upload.\n")
    
    successful_uploads = 0
    failed_uploads = 0
    
    # The API endpoint for uploads is /repo/api/v1/uploads
    upload_endpoint = f"{FOSSOLOGY_URL}/repo/api/v1/uploads"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # Loop through the list of found zip files and upload each one.
    for index, file_name in enumerate(zip_files_to_upload):
        full_path = os.path.join(directory_path, file_name)
        folder_name = os.path.splitext(file_name)[0] 

        print(f"[{index + 1}/{len(zip_files_to_upload)}] Uploading '{file_name}' as project '{folder_name}'...")

        data_payload = {
            'folderName': folder_name,
            'uploadDescription': f"Batch API upload of {file_name}",
            'public': 'public',
            'uploadType': 'file' 
        }

        try:
            with open(full_path, 'rb') as f:
                files_payload = {
                    'fileInput': (file_name, f, 'application/zip')
                }

                response = requests.post(
                    upload_endpoint, 
                    headers=headers, 
                    files=data_payload, 
                    timeout=300)

            if response.status_code == 201:
                upload_id = response.json().get('id', 'N/A')
                print(f"  -> SUCCESS: Upload created with ID: {upload_id}")
                successful_uploads += 1
            else:
                print(f"  -> ERROR: Upload failed with status code {response.status_code}")
                print(f"     Response: {response.text}")
                failed_uploads += 1

        except requests.exceptions.RequestException as e:
            upload_id = response.json().get('id', 'N/A')
            print(f"  -> ERROR: A network error occurred: {e}")
            failed_uploads += 1
        except Exception as e:
            upload_id = response.json().get('id', 'N/A')
            print(f"  -> ERROR: An unexpected error occurred: {e}")
            failed_uploads += 1
        
        print("-" * 20)
        time.sleep(1)

    print("\n--- Batch Upload Complete ---")
    print(f"Successfully uploaded: {successful_uploads}")
    print(f"Failed uploads:        {failed_uploads}")
    print("---------------------------\n")