import streamlit as st

# === CONFIGURAÇÃO DA ABA DO NAVEGADOR ===
st.set_page_config(
    page_title="Chamados TI · Biocamp",
    page_icon="🖥️",
    layout="centered"
)

from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIGURAÇÕES DE E-MAIL ===
EMAIL_REMETENTE = "tecsuporteti@biocamp.com.br"
SENHA_DE_APP = "gzzi gvmq hfte hltg"  # ← Gerar se tiver 2FA
EMAIL_SUPORTE_TI = "tecsuporteti@biocamp.com.br"

# === FUNÇÃO: Enviar e-mail para o suporte ===
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

# === FUNÇÃO: Enviar confirmação para o colaborador ===
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

# === CONEXÃO COM GOOGLE SHEETS ===
creds_dict = json.loads(st.secrets["CREDENTIALS_JSON"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1VBblQeeZXF-jR4WqKk-lHtkafARmrekyss49pL6uRmQ").sheet1

# === INTERFACE STREAMLIT ===
st.title("🖥️ Abertura de Chamados - TI")

with st.form("form_chamado"):
    nome = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail")
    setor = st.selectbox("Setor", ["Financeiro", "RH", "TI", "Logística", "Outro"])
    problema = st.text_area("Descreva o problema")
    enviado = st.form_submit_button("Enviar chamado")

# === LÓGICA DE ENVIO ===
if enviado:
    if not nome or not email or not problema:
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")
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
