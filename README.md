# File Processing Pipeline - Step 1: Upload and Extraction Interface

This project represents the first step in a modular file processing pipeline. It provides a user-friendly interface for uploading and processing images via local files or Google Drive links. The application consists of two main components:

- **Frontend:** A Streamlit-based user interface.
- **Backend:** A FastAPI service that processes uploaded files.

---

## Features

- Download images from a Google Drive folder
- Extract images from `.zip` or `.tar` archives
- Support for direct upload of `.jpg`, `.jpeg`, and `.png` images
- Displays success and error messages to users

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/FerhatAkkopru/pipline
cd pipline
```

### 2. Set Up Virtual Environment and Install Requirements

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create the `secret.env` File

To use the Google Drive API, you'll need an API key. Create a `.env` file and add your key:

```
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```

---

## Running the Application

### 1. Start the Backend (FastAPI)

```bash
uvicorn fast_api:app --reload
```

### 2. Start the Frontend (Streamlit)

```bash
streamlit run basic_ui.py
```
## Project Structure

```
.
├── basic_ui.py             # Streamlit frontend interface
├── fast_api.py         # FastAPI backend service
├── secret.env         # Contains your Google API key
├── uploads/           # Directory for uploaded or downloaded files
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## Technologies Used

- Python
- Streamlit
- FastAPI
- Requests
- Google Drive API

---

## Feedback

Feel free to open an [issue](https://github.com/FerhatAkkopru/pipline/issues) for questions, suggestions, or bug reports.
