import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

# ====== CONFIGURAÇÃO DA PÁGINA ======
st.set_page_config(
    page_title="Canal de Denúncias · Biocamp",
    page_icon="📢",
    layout="centered"
)

# ====== FUNÇÃO: Converter imagem em base64 para exibir no app ======
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def show_logo(logo_path, width=350):
    img_base64 = get_base64_of_bin_file(logo_path)
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src='data:image/png;base64,{img_base64}' width='{width}'/>
        </div>
        """,
        unsafe_allow_html=True
    )

# ====== EXIBIR O LOGO DA EMPRESA ======
show_logo("canal_denuncias/logo-LGPD.png", width=350)

# ====== INTEGRAÇÃO COM GOOGLE SHEETS ======
creds_dict = st.secrets["google"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1tMnVMHoafuuVmzpUPG2gLhKyCWEOCvtzaWBD5KBMUQc").sheet1

# ====== INTERFACE DO APP ======
st.title("📢 Canal de Denúncias Anônimas")
st.markdown(
    "Este é um canal confidencial para registrar denúncias internas. "
    "Todas as informações são tratadas com seriedade e sigilo absoluto."
)

# ====== FORMULÁRIO DE ENVIO ======
with st.form("form_denuncia"):
    denuncia = st.text_area("Descreva sua denúncia de forma anônima:", height=200)
    enviado = st.form_submit_button("Enviar denúncia")

# ====== LÓGICA DE ENVIO ======
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
