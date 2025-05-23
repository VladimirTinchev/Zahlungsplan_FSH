
import streamlit as st
import openai
import os
import pdfplumber

# GPT-Modell dynamisch auswählen
def select_model():
    try:
        openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": "Ping"}],
            temperature=0
        )
        return "gpt-4-turbo"
    except Exception:
        return "gpt-3.5-turbo"

model = select_model()
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🧠 GPT Zahlungsplan-Assistent")

uploaded_files = st.file_uploader("📁 Rechnungen hochladen", type="pdf", accept_multiple_files=True)
if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")

    all_text = ""
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"

    st.markdown("### 📄 Extrahierter Text")
    st.text_area("Hier könnte der extrahierte Text stehen.", value=all_text.strip(), height=300)

    if st.button("🔍 Analysiere mit GPT"):
        with st.spinner("Analysiere..."):
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": all_text.strip()}
                    ],
                    temperature=0
                )
                result = response.choices[0].message.content
                st.markdown("### 💡 Analyse-Ergebnis")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Fehler bei der Analyse: {e}")
