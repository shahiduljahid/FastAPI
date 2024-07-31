import os
import gdown


async def download_file_if_needed(FILE_PATH, FILE_URL):
    if not os.path.exists(FILE_PATH):
        print(f"File not found. Downloading from {FILE_URL}...")
        gdown.download(FILE_URL, FILE_PATH, quiet=False)
        if os.path.exists(FILE_PATH):
            print(f"File downloaded successfully and saved to {FILE_PATH}")
        else:
            print("Failed to download file.")
    else:
        print("File already exists. No download needed.")
