import streamlit as st
from docx import Document
from io import BytesIO

st.title("Editor de Contrato")

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

        # Criar um novo arquivo .docx em memória
        output = BytesIO()
        doc.save(output)
        output.seek(0)

        # Botão de download
        st.download_button(
            label="Baixar Documento Modificado",
            data=output,
            file_name="contrato_editado.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
