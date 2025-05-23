
import streamlit as st
import pdfplumber
import openai
import os

st.set_page_config(page_title="Zahlungsplan Generator", layout="wide")
st.title("🧠 GPT Zahlungsplan-Assistent")
st.markdown("📂 **Rechnungen hochladen**")

uploaded_files = st.file_uploader("Drag and drop files here", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")
    extracted_text = ""
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"

    st.markdown("## 🧾 Extrahierter Text")
    st.text_area("Hier könnte der extrahierte Text stehen.", value=extracted_text, height=300)

    if st.button("🔍 Analysiere mit GPT"):
        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"Hier ist eine Rechnung oder mehrere Rechnungen:\n{extracted_text}\nBitte extrahiere Name, Adresse, Mietkosten, Werbekosten, Gastro-Kosten, Kontoinformationen."}
                ],
                temperature=0
            )
            analysis = response.choices[0].message.content
            st.markdown("### 📊 Analyse-Ergebnis")
            st.write(analysis)
        except Exception as e:
            st.error(f"Fehler bei der Analyse: {e}")
