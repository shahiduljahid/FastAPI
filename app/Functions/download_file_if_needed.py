import os
import gdown
import asyncio
from concurrent.futures import ThreadPoolExecutor


async def download_file_if_needed(FILE_PATH, FILE_URL):
    if not os.path.exists(FILE_PATH):
        print(f"File not found. Downloading from {FILE_URL}...")

        # Run the synchronous download in a thread
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, gdown.download, FILE_URL, FILE_PATH, False)

        if os.path.exists(FILE_PATH):
            print(f"File downloaded successfully and saved to {FILE_PATH}")
        else:
            print("Failed to download file.")
    else:
        print("File already exists. No download needed.")
