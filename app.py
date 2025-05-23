import streamlit as st
import pdfplumber
import openai
import os

# GPT API Key aus Secret-Feld (Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Zahlungsplan-Analyse mit GPT")
st.title("📄 GPT-Zahlungsplan Assistent")
st.markdown("Bitte lade 1–3 PDF-Rechnungen hoch. GPT analysiert die Inhalte und erstellt eine strukturierte Übersicht.")

# Upload
uploaded_files = st.file_uploader("Rechnungen hochladen", type="pdf", accept_multiple_files=True)

# PDF-Inhalte auslesen
def extract_text_from_pdfs(files):
    all_text = ""
    for file in files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
    return all_text

# GPT-Analyse (angepasster Prompt!)
def analyze_text_with_gpt(text):
    prompt = f"""
Du bist ein deutscher Buchhalter. Analysiere die untenstehenden PDF-Rechnungen und gib eine übersichtliche Tabelle mit folgenden Spalten zurück:

Monat | Miete + NK (brutto) | Werbebeitrag (brutto) | Gastro (brutto) | Monatlich insgesamt

Wenn möglich, verwende die gefundenen Beträge. Falls etwas nicht vorhanden ist, lass das Feld leer. Gib die Tabelle direkt im Text zurück.

TEXT DER RECHNUNGEN:
{text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# Hauptlogik
if uploaded_files and st.button("📊 Analyse starten"):
    with st.spinner("PDF-Inhalte werden analysiert..."):
        full_text = extract_text_from_pdfs(uploaded_files)
        result = analyze_text_with_gpt(full_text)
    st.success("✅ Analyse abgeschlossen:")
    st.markdown(result)