import streamlit as st

# ✅ Este comando deve ser o PRIMEIRO do Streamlit
st.set_page_config(
    page_title="Canal de Denúncias · Biocamp",
    page_icon="📢",
    layout="centered"
)

from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Autenticação com Google Sheets ===
creds_dict = st.secrets["google"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1tMnVMHoafuuVmzpUPG2gLhKyCWEOCvtzaWBD5KBMUQc").sheet1

# === Interface do app ===
st.title("📢 Canal de Denúncias Anônimas")
st.markdown(
    "Este é um canal confidencial para registrar denúncias internas. "
    "Todas as informações são tratadas com seriedade e sigilo absoluto."
)

# === Formulário de envio ===
with st.form("form_denuncia"):
    denuncia = st.text_area("Descreva sua denúncia de forma anônima:", height=200)
    enviado = st.form_submit_button("Enviar denúncia")

# === Lógica de envio ===
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
