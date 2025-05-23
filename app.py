import streamlit as st
from openai import OpenAI
import PyPDF2

st.set_page_config(page_title="GPT Zahlungsplan-Assistent")
st.title("🧠 GPT Zahlungsplan-Assistent")

uploaded_files = st.file_uploader("Rechnungen hochladen", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")

    st.subheader("📄 Extrahierter Text")
    extracted_text = ""

    for file in uploaded_files:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"

    st.text_area("Hier könnte der extrahierte Text stehen.", value=extracted_text, height=300)

    if st.button("🔍 Analysiere mit GPT"):
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"Hier ist eine Rechnung oder mehrere Rechnungen:
{extracted_text}"}],
                temperature=0
            )
            st.subheader("🧾 GPT Analyse")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Fehler bei der Analyse: {e}")