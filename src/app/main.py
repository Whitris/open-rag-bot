import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from PIL import Image

from src.core.loader import load_index, load_csv
from src.services import get_embedding_client, get_llm_client
from src.core.prompt import build_prompt
from src.core.retriever import retrieve_relevant_docs
from src.config.settings import csv_path, index_path

st.set_page_config(layout="wide", page_title="ASP Bot")

col1, col2, col3 = st.columns([1, 9, 1])
with col1:
    st.title("ASP Bot")
with col3:
    st.image(Image.open("src/assets/logo_asp.png"), width=200)

@st.cache_resource
def get_clients():
    embedding_client = get_embedding_client()
    llm_client = get_llm_client()
    index = load_index(index_path)
    stuff = load_csv(csv_path)
    return embedding_client, llm_client, index, stuff

embedding_client, llm_client, index, stuff = get_clients()

if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "Sei un assistente virtuale. Rispondi sempre in italiano."}
    ]

st.write("Fai una domanda sui documenti ASP:")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Scrivi qui la tua domanda...")
    submitted = st.form_submit_button("Invia")
    if submitted and user_input.strip():
        question = user_input.strip()
        st.session_state.history.append({"role": "user", "content": question})

        with st.spinner("Sto ragionando..."):
            retrieved_docs = retrieve_relevant_docs(question, embedding_client, index, stuff, k=5)
            context = " ".join(retrieved_docs)
            prompt = build_prompt(question, context)
            st.session_state.history.append({"role": "system", "content": prompt})
            response = llm_client.generate_response(st.session_state.history)
            st.session_state.history.append({"role": "assistant", "content": response})

# Mostra la chat (cronologica)
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**🧑‍💼 Utente:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🤖 Bot:** {msg['content']}")
    # Non mostrare i messaggi di tipo 'system'

if st.button("Resetta conversazione"):
    st.session_state.history = [
        {"role": "system", "content": "Sei un assistente virtuale. Rispondi sempre in italiano."}
    ]
    st.rerun()

