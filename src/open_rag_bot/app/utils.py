from pathlib import Path
import zipfile

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def get_collection_dir(file: UploadedFile, dir: str):
    dir = Path(dir)
    zip_path = dir / "collection.zip"
    with open(zip_path, "wb") as f:
        f.write(file.getbuffer())
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dir)
    subdirs = [p for p in dir.iterdir() if p.is_dir()]
    if not subdirs:
        st.error("No directory found in ZIP. Please upload a valid index ZIP.")
        st.stop()
    collection_dir = subdirs[0]

    subdirs = [p for p in collection_dir.iterdir() if p.is_dir()]

    return collection_dir
