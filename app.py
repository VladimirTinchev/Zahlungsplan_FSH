import streamlit as st
import openai

st.set_page_config(page_title="Zahlungsplan Assistent", layout="centered")

st.title("🧠 GPT Zahlungsplan-Assistent")
st.markdown("#### 📤 Rechnungen hochladen")
uploaded_files = st.file_uploader("Drag and drop files here", accept_multiple_files=True, type="pdf")

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")

    st.markdown("### 📝 Extrahierter Text")
    extracted_text = "Hier könnte der extrahierte Text stehen."
    st.text_area("Extrahierter Text", value=extracted_text, height=200)

    if st.button("🔍 Analysiere mit GPT"):
        with st.spinner("Analysiere mit GPT..."):
            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": f"Hier ist eine Rechnung oder mehrere Rechnungen:
{extracted_text}"}
                    ],
                    temperature=0
                )
                gpt_response = response.choices[0].message.content
                st.success("✅ Analyse abgeschlossen.")
                st.text_area("💬 GPT Antwort", value=gpt_response, height=300)
            except Exception as e:
                st.error(f"❌ Fehler bei der Analyse:

{e}")