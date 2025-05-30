import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

# ====== CONFIGURAÇÃO DO TÍTULO E ÍCONE DA ABA ======
st.set_page_config(
    page_title="Chamados TI · Biocamp",
    page_icon="🖥️"
)

# ====== FUNÇÃO: Converter imagem em base64 para exibir no app ======
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def show_logo(logo_path, width=200):
    img_base64 = get_base64_of_bin_file(logo_path)
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src='data:image/jpg;base64,{img_base64}' width='{width}'/>
        </div>
        """,
        unsafe_allow_html=True
    )

# ====== EXIBIR O LOGO ======
show_logo("chamados_ti/LOGO BIOCAMP EM JPG.jpg")

# ====== CONFIGURAÇÕES DO E-MAIL ======
EMAIL_REMETENTE = "tecsuporteti@biocamp.com.br"
SENHA_DE_APP = "gzzi gvmq hfte hltg"  # ← Geração obrigatória se conta tiver 2FA
EMAIL_SUPORTE_TI = "tecsuporteti@biocamp.com.br"

# ====== FUNÇÃO: Enviar e-mail para o suporte TI ======
def enviar_para_suporte(nome, email, setor, problema):
    assunto = f"[CHAMADO] {nome} - Setor: {setor}"
    corpo = f"""
    Um novo chamado foi registrado no sistema:

    📌 Nome: {nome}
    📧 E-mail: {email}
    🏢 Setor: {setor}
    📝 Descrição:
    {problema}

    [Enviado automaticamente pelo sistema Streamlit]
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_SUPORTE_TI
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_REMETENTE, SENHA_DE_APP)
    server.sendmail(EMAIL_REMETENTE, EMAIL_SUPORTE_TI, msg.as_string())
    server.quit()

# ====== FUNÇÃO: Enviar confirmação ao colaborador ======
def enviar_confirmacao(nome, email, setor):
    assunto = "✅ Chamado registrado com sucesso"
    corpo = f"""
    Olá, {nome}!

    Seu chamado foi registrado com sucesso para o setor {setor}.
    A equipe de TI analisará sua solicitação em breve.

    Obrigado pelo contato!

    [Mensagem automática - não responda este e-mail]
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = email
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_REMETENTE, SENHA_DE_APP)
    server.sendmail(EMAIL_REMETENTE, email, msg.as_string())
    server.quit()

# ====== INTEGRAÇÃO COM GOOGLE SHEETS (via secrets) ======
creds_dict = json.loads(st.secrets["CREDENTIALS_JSON"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1VBblQeeZXF-jR4WqKk-lHtkafARmrekyss49pL6uRmQ").sheet1

# ====== INTERFACE STREAMLIT ======
st.title("Abertura de Chamados - TI")

with st.form("form_chamado"):
    nome = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail")
    setor = st.selectbox("Setor", ["Financeiro", "RH", "TI", "Logística", "Outro"])
    problema = st.text_area("Descreva o problema")
    enviado = st.form_submit_button("Enviar chamado")

if enviado:
    if not nome or not email or not problema:
        st.warning("Por favor, preencha todos os campos obrigatórios.")
    else:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        novo_chamado = [data, nome, email, setor, problema, "Aberto"]

        try:
            sheet.append_row(novo_chamado)
        except Exception as e:
            st.error(f"❌ Erro ao registrar o chamado no Google Sheets: {e}")
        else:
            try:
                enviar_para_suporte(nome, email, setor, problema)
                enviar_confirmacao(nome, email, setor)
                st.success("✅ Chamado registrado e e-mails enviados com sucesso!")
            except Exception as e:
                st.warning(f"⚠️ Chamado registrado, mas houve erro ao enviar os e-mails: {e}")
