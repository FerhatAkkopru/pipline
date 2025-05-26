import os
import streamlit as st
import requests

st.set_page_config(page_title="Upload File", page_icon="📤", layout="centered")

col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("document.png", width=60)
with col2:
    st.markdown("<h2 style='vertical-align: middle; margin-bottom:0px;'>Upload File</h2>", unsafe_allow_html=True)

FILE_TYPES = ["Drive Link", "Zip", "Tar", "Image"]
API_URL = "http://127.0.0.1:8000/upload"

st.write("")

## Select file type
selected_type = st.selectbox(
    "Select file type:",
    FILE_TYPES,
    help="Select the format of the file you want to upload."
)

# Initialize variables for uploaded files and drive link
uploaded_files = None
drive_link = ""

st.write("")


# Input fields based on selected file type
if selected_type == "Drive Link":
    drive_link = st.text_input(
        "🔗 Enter Google Drive folder link:",
        placeholder="https://drive.google.com/drive/folders/..."
    )
else:
    # For Zip, Tar, or Image file uploads
    allowed_exts = {
        "Zip": ["zip"],
        "Tar": ["tar"],
        "Image": ["jpg", "jpeg", "png"]
    }
    upload_label = f"📎 Select a {selected_type.lower()} file"
    if selected_type == "Image":
        upload_label = f"🖼️ Select image files"

    uploaded_files = st.file_uploader(
        upload_label,
        type=allowed_exts.get(selected_type, []),
        accept_multiple_files=(selected_type == "Image")
    )

st.write("")

# Button to send the file or link
if st.button("Send", use_container_width=True):
    if selected_type == "Drive Link":
        if not drive_link:
            st.warning("⚠️ Please enter a valid Drive folder link!")
        else:
            try:
                # Validate the Drive link format
                with st.spinner('Downloading images from Drive...'):
                    response = requests.post(API_URL, data={"type": "drive", "link": drive_link})
                    response.raise_for_status()
                response_json = response.json()
                ## Check if the response contains an error message
                st.success(f"✅ {response_json.get('status', 'Success!')}")
                ## Display the number of images downloaded and the folder path
                if "count" in response_json:
                    st.info(f"🖼️ {response_json['count']} image(s) downloaded to folder: `{response_json['folder']}`")
            ## Handle specific exceptions for better error messages
            except requests.exceptions.HTTPError as http_err:
                st.error(f"❌ HTTP Error: {http_err} - Server response: {response.text}")
            except requests.exceptions.RequestException as req_err:
                st.error(f"❌ Connection Error: {req_err}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")

    else:
        # For Zip, Tar, or Image file uploads
        if not uploaded_files:
            st.warning(f"⚠️ Please upload a {selected_type} file.")
        else:
            # Normalize the filename for single file uploads
            filename = uploaded_files.name.lower() if not isinstance(uploaded_files, list) else None
            # Check if the file extension is valid
            allowed_exts = {
                "Zip": ["zip"],
                "Tar": ["tar"],
                "Image": ["jpg", "jpeg", "png"]
            }
            # Check if the uploaded file(s) match the allowed extensions
            if selected_type == "Image":
                files = [uploaded_files] if not isinstance(uploaded_files, list) else uploaded_files
                invalid_ext = [f.name for f in files if os.path.splitext(f.name)[1][1:].lower() not in allowed_exts[selected_type]]
                if invalid_ext:
                    st.error(f"❌ Invalid file extension in: {', '.join(invalid_ext)}")
                    st.stop()
                try:
                    # Handle multiple image files
                    with st.spinner('Uploading...'):
                        files_payload = [("files", (file.name, file, file.type)) for file in files]
                        response = requests.post(API_URL, data={"type": "image"}, files=files_payload)
                        response.raise_for_status()
                    response_json = response.json()
                    st.success(f"✅ {response_json.get('status', 'Success!')}")
                    st.info(f"🖼️ {response_json.get('count', 0)} image(s) uploaded.")
                except Exception as e:
                    st.error(f"❌ Upload failed: {e}")
            else:
                # Handle single file uploads for Zip or Tar
                file_to_send = uploaded_files if not isinstance(uploaded_files, list) else uploaded_files[0]
                ext = os.path.splitext(file_to_send.name)[1][1:].lower()
                if ext not in allowed_exts[selected_type]:
                    st.error(f"❌ Invalid file extension. Expected {selected_type.lower()} file.")
                else:
                    try:
                        # Send the file to the API
                        with st.spinner('Uploading...'):
                            files_payload = {"file": (file_to_send.name, file_to_send, file_to_send.type)}
                            response = requests.post(API_URL, data={"type": selected_type.lower()}, files=files_payload)
                            response.raise_for_status()
                        # Parse the response
                        response_json = response.json()
                        # Check if the response contains an error message
                        st.success(f"✅ {response_json.get('status', 'Success!')}")
                        st.info(f"Extracted files: {', '.join(response_json.get('files', []))}")
                    except Exception as e:
                        st.error(f"❌ Upload failed: {e}")
