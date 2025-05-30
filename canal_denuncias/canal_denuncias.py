import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

# ✅ Este comando deve ser o PRIMEIRO do Streamlit
st.set_page_config(
    page_title="Canal de Denúncias · Biocamp",
    page_icon="📢",
    layout="centered"
)

# === Função para converter imagem em base64 ===
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

# === Exibir logo ===
show_logo("canal_denuncias/logo-LGPD.png", width=350)

# === Autenticação com Google Sheets ===
creds_dict = st.secrets["google"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1tMnVMHoafuuVmzpUPG2gLhKyCWEOCvtzaWBD5KBMUQc").sheet1

# === Interface do app ===
st.title("📢 Canal de Denúncias Anônimas")
st.markdown(
    """
    O canal de denúncias da empresa existe para garantir um ambiente de trabalho íntegro, seguro e respeitoso. 
    Por isso, pedimos a todos os colaboradores que façam uso deste recurso com responsabilidade.

    Denúncias devem ser feitas de forma consciente, verdadeira e com boa fé. 
    O canal não é espaço para fofocas, intrigas ou acusações infundadas. 
    O mau uso pode comprometer a credibilidade do sistema e prejudicar pessoas injustamente.

    **Lembre-se:** usar o canal de forma incorreta também é uma violação ética.

    Contamos com a sua seriedade. Juntos, manteremos um ambiente justo para todos.
    """
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
