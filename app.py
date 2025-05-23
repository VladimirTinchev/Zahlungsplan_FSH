import streamlit as st
from openai import OpenAI
import pdfplumber
import tempfile

st.set_page_config(page_title="GPT Zahlungsplan-Assistent")
st.title("🧠 GPT Zahlungsplan-Assistent")

uploaded_files = st.file_uploader("📂 Rechnungen hochladen", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")
    extracted_texts = []
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            extracted_texts.append(text)
    full_text = "\n\n".join(extracted_texts)
    st.subheader("📄 Extrahierter Text")
    st.text_area("Hier könnte der extrahierte Text stehen.", full_text, height=300)

    if st.button("🔍 Analysiere mit GPT"):
        with st.spinner("GPT analysiert die Inhalte..."):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"Hier ist eine Rechnung oder mehrere Rechnungen:
{full_text}
Welche Beträge sind monatlich zu zahlen für Miete, Werbung, Gastro? Zeige sie als Tabelle."}
                ],
                temperature=0
            )
            antwort = response.choices[0].message.content
            st.success("✅ Analyse abgeschlossen.")
            st.markdown("### 🧾 GPT-Auswertung")
            st.markdown(antwort)
