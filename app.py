import streamlit as st
import openai

st.set_page_config(page_title="Zahlungsplan GPT", layout="centered")
st.title("📄 GPT Zahlungsplan-Assistent")
st.markdown("#### 📁 Rechnungen hochladen")

uploaded_files = st.file_uploader(
    "Drag and drop files here", type=["pdf"], accept_multiple_files=True
)

if uploaded_files:
    st.success("✅ Die Rechnungen wurden erfolgreich hochgeladen.")

    # Hier kann ein Mock-Text angezeigt werden (z. B. extrahierter Text)
    st.markdown("### 📝 Extrahierter Text")
    extracted_text = "Hier könnte der extrahierte Text stehen.
(Beispielhafter Platzhalterinhalt.)"
    st.text_area("Extrahierter Text", extracted_text, height=250)

    if st.button("🔍 Analysiere mit GPT"):
        try:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"Hier ist eine Rechnung oder mehrere Rechnungen:
{extracted_text}"}
                ],
                temperature=0,
            )
            st.markdown("### 🧠 Analyse")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Fehler bei der Analyse: {e}")