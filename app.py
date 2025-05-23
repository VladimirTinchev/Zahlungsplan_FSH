import streamlit as st
import fitz  # PyMuPDF
import openai
import os

st.set_page_config(page_title="GPT Zahlungsplan-Assistent", layout="wide")
st.title("🧠 GPT Zahlungsplan-Assistent")
st.subheader("📂 Rechnungen hochladen")

uploaded_files = st.file_uploader("Drag and drop files here", accept_multiple_files=True, type=["pdf"])
extracted_text = ""

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")
    st.markdown("### 📄 Extrahierter Text")
    for uploaded_file in uploaded_files:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                extracted_text += page.get_text()

    st.text_area("Hier könnte der extrahierte Text stehen.", extracted_text, height=300)

    if st.button("🔍 Analysiere mit GPT"):
        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Hier ist eine Rechnung oder mehrere Rechnungen:
{extracted_text}"
                }]
            )
            gpt_response = response['choices'][0]['message']['content']
            st.markdown("### 🧾 Analyse-Ergebnis")
            st.write(gpt_response)
        except Exception as e:
            st.error(f"Fehler bei der Analyse: {e}")