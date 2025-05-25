import re
import requests
import os

# 1. Drive link doğrulama fonksiyonu
def is_valid_drive_link(link: str) -> bool:
    # Basit regex ile kontrol (file veya folder)
    pattern = r"https://drive\.google\.com/(file/d/|open\?id=|drive/folders/)[\w-]+"
    return bool(re.match(pattern, link))


# 2. Google Drive dosyasından resim indirme
#    NOT: Bu sadece paylaşıma açık, direkt indirilebilir dosyalar içindir.
def download_drive_images(drive_link: str, save_folder: str) -> list:
    """
    Google Drive linkinden dosya ID çıkarır,
    eğer bu ID bir resimse indirir, ya da zip/tar ise açıp resimleri çeker.
    Sadece jpeg/jpg/png kabul edilir.
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    file_id = extract_file_id(drive_link)
    if not file_id:
        raise ValueError("Geçerli bir dosya ID'si bulunamadı.")

    # İndirilebilir link oluştur
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # İlk isteği yap
    session = requests.Session()
    response = session.get(download_url, stream=True)
    
    # Google Drive büyük dosya veya virüs kontrol sayfası için token kontrolü
    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(download_url, params=params, stream=True)
    
    content_type = response.headers.get('Content-Type', '')
    if not any(x in content_type for x in ['image/jpeg', 'image/png', 'application/zip', 'application/x-tar']):
        raise ValueError(f"Desteklenmeyen dosya türü: {content_type}")

    # Dosya adı belirleme (kaba)
    file_name = f"{file_id}"
    if 'image/jpeg' in content_type:
        file_name += ".jpg"
    elif 'image/png' in content_type:
        file_name += ".png"
    elif 'application/zip' in content_type:
        file_name += ".zip"
    elif 'application/x-tar' in content_type:
        file_name += ".tar"

    file_path = os.path.join(save_folder, file_name)
    save_response_content(response, file_path)

    # Eğer zip veya tar ise içinden resimleri çıkar (daha önce verdiğim extract fonksiyonlarını kullanabilirsin)
    images_extracted = []
    if file_name.endswith(".zip"):
        from zipfile import ZipFile
        with ZipFile(file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if os.path.splitext(file)[1].lower() in [".jpg", ".jpeg", ".png"]:
                    extracted_path = os.path.join(save_folder, file)
                    with open(extracted_path, "wb") as f:
                        f.write(zip_ref.read(file))
                    images_extracted.append(extracted_path)

    elif file_name.endswith(".tar"):
        import tarfile
        with tarfile.open(file_path, "r") as tar_ref:
            for member in tar_ref.getmembers():
                if os.path.splitext(member.name)[1].lower() in [".jpg", ".jpeg", ".png"]:
                    tar_ref.extract(member, save_folder)
                    images_extracted.append(os.path.join(save_folder, member.name))

    elif file_name.endswith((".jpg", ".jpeg", ".png")):
        images_extracted.append(file_path)

    return images_extracted


def extract_file_id(drive_link: str) -> str:
    """
    Drive linkten file ID'yi çıkarır
    """
    patterns = [
        r"https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
        r"https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",
        r"https://drive\.google\.com/uc\?id=([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, drive_link)
        if match:
            return match.group(1)
    return ""

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination, chunk_size=32768):
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)

