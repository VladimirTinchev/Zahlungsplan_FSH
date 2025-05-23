
import streamlit as st
import openai
import pdfplumber

st.set_page_config(page_title="Zahlungsplan GPT", layout="centered")
st.title("🧠 GPT Zahlungsplan-Assistent")

uploaded_files = st.file_uploader("📄 Rechnungen hochladen", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.info("Die Rechnungen wurden erfolgreich hochgeladen.")
    extracted_texts = []

    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            extracted_texts.append(text)

    full_text = "\n".join(extracted_texts)
    st.text_area("📜 Extrahierter Text", full_text[:3000], height=300)

    if st.button("🧠 Analysiere mit GPT"):
        with st.spinner("GPT analysiert die Rechnungen..."):
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du bist ein Experte für Finanzdokumente."},
                    {"role": "user", "content": f"Analysiere diese Rechnungen und extrahiere: Mietername, Adresse, Vertragsnummer, Miete+NK, Werbebeitrag, Gastro. Antworte in Tabellenformat.\n{full_text}"}
                ]
            )
            st.markdown("### Ergebnis")
            st.markdown(response['choices'][0]['message']['content'])
