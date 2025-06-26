from extract_repos import extract_repos_zip
<<<<<<< HEAD
from auth import authenticate

if __name__ == '__main__':
    extract_repos_zip()
    authenticate()
=======
from upload_repo_fossology import upload_all_zips_in_directory

zip_path = "files"

if __name__ == '__main__':
    #print("--- STEP 1: Starting to download repositories... ---")
    #print("This will take a while. Please wait for it to complete.")
    #extract_repos_zip()
    #print("\n--- STEP 1: COMPLETE. All repositories have been downloaded. ---")

    print("\n--- STEP 2: Starting to upload files to FOSSology... ---")
    upload_all_zips_in_directory(zip_path)
    print("\n--- STEP 2: COMPLETE. All files have been uploaded. ---")
    print("\nProcess finished.")
>>>>>>> 1516627 (feat: fossology)
