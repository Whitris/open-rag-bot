import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from PIL import Image

from src.config.settings import icon_path
from src.core.chat_bot import get_chat_bot

st.set_page_config(layout="wide", page_title="Open Rag Bot")

col1, col2, col3 = st.columns([4, 4, 4])
with col1:
    st.title("Open Rag Bot")
with col3:
    if icon_path is not None:
        st.image(Image.open(icon_path), width=200)
    else:
        st.text("")

if "history" not in st.session_state:
    st.session_state.history = [
        {
            "role": "system",
            "content": "You are a virtual assistant. Always answer in the question language.",
        }
    ]

if "chat_bot" not in st.session_state:
    st.session_state.chat_bot = get_chat_bot(st.session_state.history)
else:
    st.session_state.chat_bot.history = st.session_state.history

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Write here your question...")
    submitted = st.form_submit_button("Ask")
    if submitted and user_input.strip():
        question = user_input.strip()
        with st.spinner("I am thinking..."):
            response = st.session_state.chat_bot.answer(question=question)

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**🧑‍💼 User:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🤖 Bot:** {msg['content']}")

if st.button("Reset conversation"):
    st.session_state.history = [
        {
            "role": "system",
            "content": "You are a virtual assistant. Always answer in the question language.",
        }
    ]
    st.rerun()
