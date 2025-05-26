import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv("secret.env")

# Load Google API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

## Validate Google Drive folder ID
def is_valid_drive_folder_id(folder_id):
    return len(folder_id) >= 10

# List images in a Google Drive folder
def list_drive_images(folder_id):
    url = "https://www.googleapis.com/drive/v3/files"
    query = f"'{folder_id}' in parents and (mimeType='image/jpeg' or mimeType='image/png') and trashed=false"
    params = {
        "q": query,
        "fields": "files(id, name, mimeType)",
        "key": GOOGLE_API_KEY,
    }
    ## Make a request to the Google Drive API to list files
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Drive API error: {r.text}")
    return r.json().get("files", [])

# Download a file from Google Drive
def download_drive_file(file_id):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={GOOGLE_API_KEY}"
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Drive file download error: {r.text}")
    return r.content
