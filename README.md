# File Processing Pipeline - Step 1: Upload and Extraction Interface
# Dosya İşleme Boru Hattı - Adım 1: Yükleme ve Çıkarma Arayüzü

This project represents the first crucial step in a modular file processing pipeline. It offers a user-friendly interface designed to upload and process images sourced from local files or Google Drive links. The application is structured with two primary components:
Bu proje, modüler bir dosya pipline hattının ilk önemli adımını temsil eder. Yerel dosyalardan veya Google Drive bağlantılarından alınan görüntüleri yüklemek ve işlemek için tasarlanmış kullanıcı dostu bir arayüz sunar. Uygulama iki ana bileşenle yapılandırılmıştır:

-   **Frontend:** A Streamlit-based user interface for easy interaction.
    **Frontend:** Kolay etkileşim için Streamlit tabanlı bir kullanıcı arayüzü.
-   **Backend:** A FastAPI service that handles the logic of file processing and extraction.
    **Backend:** Dosya işleme ve çıkarma mantığını yöneten bir FastAPI servisi.

---

## ✨ Features / Özellikler

-   **Google Drive Integration / Google Drive Entegrasyonu:**
    -   Download images directly from a specified Google Drive folder.
        Belirtilen bir Google Drive klasöründen doğrudan görüntü indirme.
-   **Archive Support / Arşiv Desteği:**
    -   Extract images from `.zip` and `.tar` archives.
        `.zip` ve `.tar` arşivlerinden görüntüleri çıkarma.
-   **Direct Image Upload / Doğrudan Görüntü Yükleme:**
    -   Supports direct upload of common image formats: `.jpg`, `.jpeg`, and `.png`.
        Yaygın görüntü formatlarının (`.jpg`, `.jpeg`, `.png`) doğrudan yüklenmesini destekler.
-   **Organized Storage / Düzenli Depolama:**
    -   Saves uploaded and extracted files with their original names into structured directories (e.g., `/uploads/image`, `/uploads/zip/[archive_name]/`).
        Yüklenen ve çıkarılan dosyaları orijinal adlarıyla yapılandırılmış dizinlere (örneğin, `/uploads/image`, `/uploads/zip/[arsiv_adi]/`) kaydeder.
-   **User Feedback / Kullanıcı Geri Bildirimi:**
    -   Provides clear success and error messages to the user during operations.
        İşlemler sırasında kullanıcıya net başarı ve hata mesajları sunar.

---

## 🚀 Getting Started

### Prerequisites / Ön Gereksinimler

-   Python 3.8+
-   Git

### 1. Clone the Repository / Repoyu Klonla

```bash
git clone https://github.com/FerhatAkkopru/pipline.git
cd pipline
```

### 2. Set Up Virtual Environment and Install Dependencies / Sanal Ortamı Kur ve Bağımlılıkları Yükle

It's recommended to use a virtual environment:
Bir sanal ortam kullanmanız önerilir:

```bash
# Create a virtual environment / Sanal bir ortam oluştur
python -m venv venv

# Activate the virtual environment / Sanal ortamı etkinleştir
# On Windows / Windows'ta:
venv\Scripts\activate
# On macOS/Linux / macOS/Linux'ta:
# source venv/bin/activate

# Install required packages / Gerekli paketleri yükle
pip install -r requirements.txt
```

### 3. Create the `secret.env` File for Google Drive API / Google Drive API için `secret.env` Dosyasını Oluştur

To enable Google Drive functionality, you need to provide your Google API Key. Create a file named `secret.env` in the project root and add your API key:
Google Drive işlevselliğini etkinleştirmek için Google API Anahtarınızı sağlamanız gerekir. Proje kök dizininde `secret.env` adında bir dosya oluşturun ve API anahtarınızı ekleyin:

```env
# filepath: c:\pip_py\secret.env
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```
**Note:** This file is included in `.gitignore` and should not be committed to your repository.
**Not:** Bu dosya `.gitignore` dosyasına dahildir ve deponuza gönderilmemelidir.

---

## 🏃 Running the Application / Uygulamayı Çalıştırma

The application consists of a backend service (FastAPI) and a frontend interface (Streamlit). You need to run both.

### 1. Start the Backend (FastAPI) / Arka Uç Servisini Başlat (FastAPI)

Open a terminal in the project root and run:
Proje kök dizininde bir terminal açın ve çalıştırın:

```bash
uvicorn fast_api:app --reload
```
The backend will typically be available at `http://127.0.0.1:8000`.
Arka uç genellikle `http://127.0.0.1:8000` adresinde mevcut olacaktır.

### 2. Start the Frontend (Streamlit) / Ön Yüzü Başlat (Streamlit)

Open another terminal in the project root and run:
Proje kök dizininde başka bir terminal açın ve çalıştırın:

```bash
streamlit run app.py
```
The Streamlit application will open in your web browser, usually at `http://localhost:8501`.
Streamlit uygulaması web tarayıcınızda, genellikle `http://localhost:8501` adresinde açılacaktır.

---

## 📂 Project Structure / Proje Yapısı

```
.
├── app.py              # Streamlit frontend user interface / Streamlit ön yüz kullanıcı arayüzü
├── fast_api.py         # FastAPI backend service / FastAPI arka uç servisi
├── drive_utils.py      # Utility functions for Google Drive API / Google Drive API için yardımcı fonksiyonlar
├── secret.env          # File containing your Google API Key (Untracked by Git) / Google API Anahtarınızı içeren dosya (Git tarafından izlenmez)
├── uploads/            # Directory where uploaded and downloaded files are stored / Yüklenen ve indirilen dosyaların saklandığı dizin
│   ├── drive/
│   ├── image/
│   ├── tar/
│   └── zip/
├── requirements.txt    # Python dependencies / Python bağımlılıkları
├── .gitignore          # Specifies intentionally untracked files that Git should ignore / Git'in yok sayması gereken, kasıtlı olarak izlenmeyen dosyaları belirtir
└── README.md           # Project documentation / Proje dokümantasyonu
```

---

## 🛠️ Technologies Used / Kullanılan Teknolojiler

-   Python
-   FastAPI (for the backend API)
-   Streamlit (for the user interface)
-   Uvicorn (ASGI server for FastAPI)
-   Python `dotenv` (for managing environment variables)
-   Google API Client Library for Python (for Google Drive integration)
-   Standard Python libraries: `os`, `io`, `zipfile`, `tarfile`

---

## 💬 Feedback and Contributions / Geri Bildirim ve Katkılar

Feel free to open an [issue](https://github.com/FerhatAkkopru/pipline/issues) for any questions, suggestions, bug reports, or feature requests. Contributions are welcome!
Herhangi bir soru, öneri, hata raporu veya özellik talebi için bir [issue](https://github.com/FerhatAkkopru/pipline/issues) açmaktan çekinmeyin. Katkılarınızı bekliyoruz!
