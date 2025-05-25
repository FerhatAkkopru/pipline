import os
import io
import zipfile
import tarfile
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv("secret.env")  # .env dosyasını yükler


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Google API Key (env'den al)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set!")

# CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def save_images_from_zip(file_bytes, base_name):
    image_exts = {".jpg", ".jpeg", ".png"}
    saved_files = []
    with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
        folder_path = os.path.join(UPLOAD_DIR, base_name)
        os.makedirs(folder_path, exist_ok=True)
        for info in z.infolist():
            name_lower = info.filename.lower()
            if os.path.splitext(name_lower)[1] in image_exts:
                z.extract(info, folder_path)
                saved_files.append(info.filename)
    return saved_files, folder_path

def save_images_from_tar(file_bytes, base_name):
    image_exts = {".jpg", ".jpeg", ".png"}
    saved_files = []
    folder_path = os.path.join(UPLOAD_DIR, base_name)
    os.makedirs(folder_path, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(file_bytes)) as tar:
        for member in tar.getmembers():
            name_lower = member.name.lower()
            if member.isfile() and os.path.splitext(name_lower)[1] in image_exts:
                tar.extract(member, folder_path)
                saved_files.append(member.name)
    return saved_files, folder_path

def is_valid_drive_folder_id(folder_id):
    # Basit ID format kontrolü (daha kapsamlı olabilir)
    return len(folder_id) >= 10

def list_drive_images(folder_id):
    url = "https://www.googleapis.com/drive/v3/files"
    query = f"'{folder_id}' in parents and (mimeType='image/jpeg' or mimeType='image/png') and trashed=false"
    params = {
        "q": query,
        "fields": "files(id, name, mimeType)",
        "key": GOOGLE_API_KEY,
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Drive API error: {r.text}")
    return r.json().get("files", [])

def download_drive_file(file_id):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={GOOGLE_API_KEY}"
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Drive file download error: {r.text}")
    return r.content

@app.post("/upload")
async def upload_file(type: str = Form(...), file: UploadFile = File(None), link: str = Form(None)):
    if type == "drive":
        if not link:
            raise HTTPException(status_code=400, detail="Drive link missing.")
        
        # Linkten folder ID çıkar (basit hali)
        try:
            folder_id = link.split("/folders/")[1].split("?")[0]
        except IndexError:
            raise HTTPException(status_code=400, detail="Invalid Drive folder link.")
        
        if not is_valid_drive_folder_id(folder_id):
            raise HTTPException(status_code=400, detail="Invalid Drive folder ID.")
        
        images = list_drive_images(folder_id)
        if not images:
            return {"status": "No images found in folder."}
        
        base_folder = os.path.join(UPLOAD_DIR, folder_id)
        os.makedirs(base_folder, exist_ok=True)
        saved_files = []
        for img in images:
            img_data = download_drive_file(img["id"])
            path = os.path.join(base_folder, img["name"])
            with open(path, "wb") as f:
                f.write(img_data)
            saved_files.append(img["name"])
        
        return {
            "status": "Drive images downloaded.",
            "count": len(saved_files),
            "folder": base_folder,
            "files": saved_files
        }

    elif file:
        contents = await file.read()
        base_name = os.path.splitext(file.filename)[0]

        if type == "zip":
            saved_files, folder = save_images_from_zip(contents, base_name)
        elif type == "tar":
            saved_files, folder = save_images_from_tar(contents, base_name)
        else:
            # Diğer dosya türleri doğrudan kaydedilir
            folder = UPLOAD_DIR
            path = os.path.join(folder, file.filename)
            with open(path, "wb") as f:
                f.write(contents)
            return {"status": "File saved", "filename": file.filename, "path": path}

        return {
            "status": "Images extracted from archive.",
            "count": len(saved_files),
            "folder": folder,
            "files": saved_files
        }
    else:
        raise HTTPException(status_code=400, detail="No valid input provided.")
