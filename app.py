import streamlit as st
from docx import Document
from io import BytesIO

st.markdown("""
    <style>
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        animation: fadeIn 1s;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stFileUploader>div>div>input {
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .icon {
        font-size: 24px;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)

st.title("Editor de Contrato")

st.markdown('<i class="icon">📄</i> Faça o upload do arquivo .docx', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="docx")

if uploaded_file:
    doc = Document(uploaded_file)

    nome_empresa = st.text_input("Nome da Empresa")
    nome_fornecedor = st.text_input("Nome do Fornecedor")

    if st.button("Gerar Documento"):
        if not nome_empresa or not nome_fornecedor:
            st.error("Por favor, preencha todos os campos.")
        else:
            for para in doc.paragraphs:
                para.text = para.text.replace("{nome_empresa}", nome_empresa)
                para.text = para.text.replace("{nome_fornecedor}", nome_fornecedor)

            output = BytesIO()
            doc.save(output)
            output.seek(0)

            st.success("Documento gerado com sucesso!")
            st.download_button(
                label="Baixar Documento Modificado",
                data=output,
                file_name="contrato_editado.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

st.markdown("</div>", unsafe_allow_html=True)
