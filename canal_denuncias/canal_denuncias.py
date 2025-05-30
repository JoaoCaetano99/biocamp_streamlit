import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# === Carregar credenciais do arquivo JSON ===
with open("credenciais.json") as f:
    creds_dict = json.load(f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ✅ ID real da sua planilha:
sheet = client.open_by_key("1tMnVMHoafuuVmzpUPG2gLhKyCWEOCvtzaWBD5KBMUQc").sheet1

# === Interface do app ===
st.set_page_config(page_title="Canal de Denúncias", layout="centered")
st.title("📢 Canal de Denúncias Anônimas")
st.markdown("Este é um canal confidencial para registrar denúncias internas. Todas as informações são tratadas com seriedade e sigilo absoluto.")

# === Formulário de envio ===
with st.form("form_denuncia"):
    denuncia = st.text_area("Descreva sua denúncia de forma anônima:", height=200)
    enviado = st.form_submit_button("Enviar denúncia")

if enviado:
    if not denuncia.strip():
        st.warning("⚠️ O campo de denúncia não pode estar vazio.")
    else:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nova_denuncia = [data, denuncia]

        try:
            sheet.append_row(nova_denuncia)
            st.success("✅ Denúncia registrada com sucesso. Obrigado pela sua colaboração.")
        except Exception as e:
            st.error(f"❌ Erro ao registrar denúncia: {e}")
