import streamlit as st
import fitz  # PyMuPDF
import openai
import os

st.set_page_config(page_title="GPT Zahlungsplan-Assistent", layout="wide")

st.title("🧠 GPT Zahlungsplan-Assistent")

st.markdown("📂 **Rechnungen hochladen**")

uploaded_files = st.file_uploader(
    "Drag and drop files here",
    type=["pdf"],
    accept_multiple_files=True,
    help="Limit 200MB per file • PDF"
)

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")

extracted_text = ""

if uploaded_files:
    st.markdown("## 🧾 Extrahierter Text")
    extracted_texts = []
    for uploaded_file in uploaded_files:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            extracted_texts.append(text)
    extracted_text = "\n\n".join(extracted_texts)
    st.text_area("Hier könnte der extrahierte Text stehen.", value=extracted_text, height=300)

    if st.button("🔍 Analysiere mit GPT"):
        try:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": f"Hier ist eine Rechnung oder mehrere Rechnungen:\n{extracted_text}"
                    }
                ],
                temperature=0
            )
            st.markdown("## 🧠 Analyse von GPT")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Fehler bei der Analyse: {e}")
