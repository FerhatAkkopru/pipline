import os
import io
import zipfile
import tarfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List
from drive_utils import is_valid_drive_folder_id, list_drive_images, download_drive_file

load_dotenv("secret.env")

app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
for sub in ["image", "zip", "tar", "drive"]:
    os.makedirs(os.path.join(UPLOAD_DIR, sub), exist_ok=True)


# CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to save images from ZIP or TAR files
def save_images_from_zip(file_bytes, base_name):
    ## Define the allowed image extensions
    image_exts = {".jpg", ".jpeg", ".png"}
    saved_files = []
    folder_path = os.path.join(UPLOAD_DIR, "zip", base_name)
    os.makedirs(folder_path, exist_ok=True)
    ## Open the ZIP file from bytes
    with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
        for info in z.infolist():
            name_lower = info.filename.lower()
            if os.path.splitext(name_lower)[1] in image_exts:
                z.extract(info, folder_path)
                saved_files.append(info.filename)
    ## Return the list of saved files and the folder path
    return saved_files, folder_path

## Function to save images from TAR files
def save_images_from_tar(file_bytes, base_name):
    ## Define the allowed image extensions
    image_exts = {".jpg", ".jpeg", ".png"}
    saved_files = []
    folder_path = os.path.join(UPLOAD_DIR, "tar", base_name)
    os.makedirs(folder_path, exist_ok=True)
    ## Open the TAR file from bytes
    with tarfile.open(fileobj=io.BytesIO(file_bytes)) as tar:
        ## Iterate through the members of the TAR file
        for member in tar.getmembers():
            name_lower = member.name.lower()
            if member.isfile() and os.path.splitext(name_lower)[1] in image_exts:
                tar.extract(member, folder_path)
                saved_files.append(member.name)
    ## Return the list of saved files and the folder path
    return saved_files, folder_path

## Endpoint to handle file uploads
@app.post("/upload")
async def upload_file(
    ## Form field to specify the type of upload
    type: str = Form(...),
    files: List[UploadFile] = File(None),
    file: UploadFile = File(None),
    link: str = Form(None)
):
    ## Validate the type of upload
    if type == "drive":
        if not link:
            raise HTTPException(status_code=400, detail="Drive link missing.")
        try:
            folder_id = link.split("/folders/")[1].split("?")[0]
        except IndexError:
            raise HTTPException(status_code=400, detail="Invalid Drive folder link.")
        if not is_valid_drive_folder_id(folder_id):
            raise HTTPException(status_code=400, detail="Invalid Drive folder ID.")
        ## List images in the specified Google Drive folder
        images = list_drive_images(folder_id)
        if not images:
            return {"status": "No images found in folder."}
        ## Create a base folder to save the images
        base_folder = os.path.join(UPLOAD_DIR, "drive", folder_id)
        os.makedirs(base_folder, exist_ok=True)
        saved_files = []
        ## Download each image from Google Drive
        for img in images:
            img_data = download_drive_file(img["id"])
            path = os.path.join(base_folder, img["name"])
            with open(path, "wb") as f:
                f.write(img_data)
            saved_files.append(img["name"])
        ## Return the status and details of the downloaded images
        return {
            "status": "Drive images downloaded.",
            "count": len(saved_files),
            "folder": base_folder,
            "files": saved_files
        }
    ## Handle the case for image uploads
    elif type == "image":
        if not files:
            raise HTTPException(status_code=400, detail="No image files provided.")

        image_dir = os.path.join(UPLOAD_DIR, "image")
        saved_files = []

        for image_file in files:
            ext = os.path.splitext(image_file.filename)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png"]:
                continue
            image_data = await image_file.read()
            path = os.path.join(image_dir, image_file.filename)
            with open(path, "wb") as f:
                f.write(image_data)
            saved_files.append(image_file.filename)

        return {
            "status": "Images uploaded.",
            "count": len(saved_files),
            "folder": image_dir,
            "files": saved_files
        }
    ## Handle ZIP or TAR file uploads
    elif file:
        contents = await file.read()
        base_name = os.path.splitext(file.filename)[0]
        ## Determine the type of archive based on the file extension
        if type == "zip":
            saved_files, folder = save_images_from_zip(contents, base_name)
        elif type == "tar":
            saved_files, folder = save_images_from_tar(contents, base_name)
        ## Return the status and details of the saved files
        return {
            "status": "Images extracted from archive.",
            "count": len(saved_files),
            "folder": folder,
            "files": saved_files
        }

    else:
        raise HTTPException(status_code=400, detail="No valid input provided.")
