import streamlit as st
from docx import Document
from io import BytesIO
import json
from streamlit_lottie import st_lottie

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.set_page_config(page_title="Editor de Contrato", layout="centered", initial_sidebar_state="collapsed")

# Injeção de CSS customizado para um design minimalista e animações sutis
custom_css = """
<style>
/* Estilo geral */
body {
    font-family: 'Helvetica Neue', sans-serif;
    background-color: #f8f9fa;
}

/* Título */
h1 {
    font-size: 2.5rem;
    color: #343a40;
    text-align: center;
    margin-bottom: 2rem;
}

/* Inputs de texto */
div.stTextInput > div > input {
    border: 2px solid #ced4da;
    border-radius: 4px;
    padding: 0.75rem;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}
div.stTextInput > div > input:focus {
    border-color: #007bff;
}

/* Uploader de arquivos */
div.stFileUploader > div {
    border: 2px dashed #ced4da;
    border-radius: 4px;
    padding: 1rem;
    background-color: #fff;
}

/* Botão primário */
button[kind="primary"] {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}
button[kind="primary"]:hover {
    background-color: #0056b3;
    transform: scale(1.02);
}

/* Botão de download */
div.stDownloadButton > button {
    background-color: #28a745;
    color: #fff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}
div.stDownloadButton > button:hover {
    background-color: #218838;
    transform: scale(1.02);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Título do aplicativo
st.title("Editor de Contrato")

# Carrega e exibe uma animação Lottie (opcional)
try:
    lottie_animation = load_lottiefile("animation.json")
    st_lottie(lottie_animation, height=150)
except Exception as e:
    st.info("Animação Lottie não encontrada ou erro ao carregar.")

# Upload do arquivo .docx
uploaded_file = st.file_uploader("Faça o upload do arquivo .docx", type="docx")

if uploaded_file:
    doc = Document(uploaded_file)

    # Campos para entrada de dados
    nome_empresa = st.text_input("Nome da Empresa")
    nome_fornecedor = st.text_input("Nome do Fornecedor")

    if st.button("Gerar Documento"):
        # Substituição dos placeholders
        for para in doc.paragraphs:
            para.text = para.text.replace("{nome_empresa}", nome_empresa)
            para.text = para.text.replace("{nome_fornecedor}", nome_fornecedor)

        # Cria um arquivo .docx em memória
        output = BytesIO()
        doc.save(output)
        output.seek(0)

        # Botão de download do documento modificado
        st.download_button(
            label="Baixar Documento Modificado",
            data=output,
            file_name="contrato_editado.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
