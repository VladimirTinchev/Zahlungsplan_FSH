
import streamlit as st
import openai
import pdfplumber

st.set_page_config(page_title="GPT Zahlungsplan-Assistent")
st.title("🧠 GPT Zahlungsplan-Assistent")

uploaded_files = st.file_uploader("📁 Rechnungen hochladen", type="pdf", accept_multiple_files=True)
texts = []

if uploaded_files:
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
            texts.append("\n".join(pages))

    full_text = "\n\n".join(texts)
    st.info("✅ Die Rechnungen wurden erfolgreich hochgeladen.")
    st.markdown("#### 📄 Extrahierter Text")
    st.code(full_text, language="markdown")

    if st.button("🔍 Analysiere mit GPT"):
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du hilfst dabei, aus Rechnungen die relevanten Zahlungsplan-Daten zu extrahieren."},
                {"role": "user", "content": full_text}
            ]
        )
        st.success("✅ Analyse abgeschlossen")
        st.markdown("### 💬 GPT-Antwort")
        st.write(response.choices[0].message.content)
