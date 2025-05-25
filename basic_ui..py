import os
import streamlit as st
import requests

st.set_page_config(page_title="Upload File", page_icon="📤", layout="centered")

# Header
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("document.png", width=60)
with col2:
    st.markdown("<h2 style='vertical-align: middle; margin-bottom:0px;'>Upload File</h2>", unsafe_allow_html=True)

FILE_TYPES = ["Drive Link", "Zip", "Tar", "Image"]
API_URL = "http://127.0.0.1:8000/upload"

st.write("")

selected_type = st.selectbox(
    "Select file type:",
    FILE_TYPES,
    help="Select the format of the file you want to upload."
)

uploaded_file = None
drive_link = ""

st.write("")

if selected_type == "Drive Link":
    drive_link = st.text_input(
        "🔗 Enter Google Drive folder link:",
        placeholder="https://drive.google.com/drive/folders/..."
    )
else:
    allowed_exts = {
        "Zip": ["zip"],
        "Tar": ["tar"],
        "Image": ["jpg", "jpeg", "png"]
    }
    upload_label = f"📎 Select a {selected_type.lower()} file"
    if selected_type == "Image":
        upload_label = f"🖼️ Select an {selected_type.lower()} file"

    uploaded_file = st.file_uploader(
        upload_label,
        type=allowed_exts.get(selected_type, []),
        accept_multiple_files=False
    )

st.write("")

if st.button("Send", use_container_width=True):
    if selected_type == "Drive Link":
        if not drive_link:
            st.warning("⚠️ Please enter a valid Drive folder link!")
        else:
            try:
                with st.spinner('Downloading images from Drive...'):
                    response = requests.post(API_URL, data={"type": "drive", "link": drive_link})
                    response.raise_for_status()
                response_json = response.json()
                st.success(f"✅ {response_json.get('status', 'Success!')}")
                if "count" in response_json:
                    st.info(f"🖼️ {response_json['count']} image(s) downloaded to folder: `{response_json['folder']}`")
            except requests.exceptions.HTTPError as http_err:
                st.error(f"❌ HTTP Error: {http_err} - Server response: {response.text}")
            except requests.exceptions.RequestException as req_err:
                st.error(f"❌ Connection Error: {req_err}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")

    else:
        if not uploaded_file:
            st.warning(f"⚠️ Please upload a {selected_type} file.")
        else:
            filename = uploaded_file.name.lower()
            ext = os.path.splitext(filename)[1][1:]
            allowed_exts = {
                "Zip": ["zip"],
                "Tar": ["tar"],
                "Image": ["jpg", "jpeg", "png"]
            }
            if ext not in allowed_exts[selected_type]:
                st.error(f"❌ Invalid file extension! Expected one of: {', '.join(allowed_exts[selected_type])}")
            else:
                try:
                    with st.spinner('Uploading...'):
                        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                        data = {"type": selected_type.lower()}
                        response = requests.post(API_URL, files=files, data=data)
                        response.raise_for_status()
                    response_json = response.json()
                    st.success(f"✅ {response_json.get('status', 'Upload successful.')}")
                    if "count" in response_json:
                        st.info(f"🖼️ {response_json['count']} image(s) extracted to folder: `{response_json['folder']}`")
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"❌ HTTP Error: {http_err} - Server response: {response.text}")
                except requests.exceptions.RequestException as req_err:
                    st.error(f"❌ Upload failed: {req_err}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {e}")

st.write("")
