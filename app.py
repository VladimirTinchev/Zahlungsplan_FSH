
import streamlit as st
import openai
import pdfplumber

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="GPT Zahlungsplan-Assistent")
st.title("🧠 GPT Zahlungsplan-Assistent")

uploaded_files = st.file_uploader("📂 Rechnungen hochladen", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")
    extracted_text = ""
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""

    st.markdown("### 📄 Extrahierter Text")
    st.text_area("Hier könnte der extrahierte Text stehen.", value=extracted_text, height=300)

    if st.button("🔍 Analysiere mit GPT"):
        with st.spinner("Analysiere…"):
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": extracted_text}],
                temperature=0
            )
            st.markdown("### 💬 GPT Antwort")
            st.write(response.choices[0].message.content)
