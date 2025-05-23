
import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📄 GPT Zahlungsplan-Assistent")

uploaded_files = st.file_uploader("Rechnungen hochladen", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success("Die Rechnungen wurden erfolgreich hochgeladen.")
    extracted_text = "Hier könnte der extrahierte Text stehen."
    st.markdown("#### 🧾 Extrahierter Text")
    st.code(extracted_text)

    if st.button("🔍 Analysiere mit GPT"):
        with st.spinner("GPT analysiert die Daten..."):
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "Extrahiere Mietername, Adresse, Vertragsnummer, Beträge aus dem Text."},
                    {"role": "user", "content": extracted_text}
                ]
            )
            result = response.choices[0].message.content
            st.markdown("#### 💡 Analyse-Ergebnis")
            st.write(result)
