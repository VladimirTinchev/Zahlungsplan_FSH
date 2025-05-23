import streamlit as st
import openai
import fitz  # PyMuPDF

st.set_page_config(page_title="GPT Zahlungsplan-Assistent")
st.title("🧠 GPT Zahlungsplan-Assistent")

st.markdown("#### 📤 Rechnungen hochladen")
uploaded_files = st.file_uploader("Drag and drop files here", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")
    extracted_text = ""
    for file in uploaded_files:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                extracted_text += page.get_text()

    st.markdown("### 📄 Extrahierter Text")
    st.text_area("Hier könnte der extrahierte Text stehen.", value=extracted_text, height=300)

    if st.button("🔍 Analysiere mit GPT"):
        prompt = f"Lies den folgenden Rechnungstext und extrahiere Mietername, Adresse, Vertragsnummer, sowie die Beträge für Miete+NK (monatlich), Werbung (halbjährlich) und Gastro (monatlich):\n\n{extracted_text}"
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        st.markdown("### 🧾 Analyse-Ergebnis")
        st.write(response.choices[0].message.content)