import streamlit as st
from docx import Document
from io import BytesIO
from streamlit_lottie import st_lottie
import json

# Configuração da Página
st.set_page_config(page_title="Editor de Contrato", page_icon="✍️", layout="wide")

# Função para carregar animações Lottie
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

# ---- BARRA SUPERIOR ----
st.markdown("""
    <style>
        .header {
            background-color: #1E1E1E;
            padding: 10px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
        .menu-container {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        .menu-button {
            background-color: transparent;
            color: white;
            border: none;
            font-size: 18px;
            margin: 0 20px;
            cursor: pointer;
            transition: color 0.3s ease;
        }
        .menu-button:hover {
            color: #FF4081;
        }
    </style>
    <div class='header'>Editor de Contrato</div>
    <div class='menu-container'>
        <button class='menu-button' onclick="window.location.href='/?page=home'">🏠 Início</button>
        <button class='menu-button' onclick="window.location.href='/?page=editor'">✍️ Editor</button>
        <button class='menu-button' onclick="window.location.href='/?page=sobre'">ℹ️ Sobre</button>
    </div>
""", unsafe_allow_html=True)

# ---- SISTEMA DE NAVEGAÇÃO ----
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]

if page == "home":
    # ---- PÁGINA INICIAL ----
    st.title("🚀 Bem-vindo ao Editor de Contratos")
    st.write("Um sistema minimalista e ultra-rápido para edição e personalização de documentos contratuais.")

    # Exibir animação Lottie
    animation = load_lottiefile("assets/animation.json")
    if animation:
        st_lottie(animation, height=200)
    else:
        st.info("Animação não encontrada.")

    st.markdown("### ✨ Comece agora mesmo!")
    st.write("Clique no menu acima para editar um contrato ou saber mais sobre o projeto.")
    st.button("Ir para o Editor de Contrato", on_click=lambda: st.experimental_set_query_params(page="editor"))

elif page == "editor":
    # ---- PÁGINA EDITOR DE CONTRATOS ----
    st.title("✍️ Editor de Contrato")

    uploaded_file = st.file_uploader("Faça o upload do arquivo .docx", type="docx")

    if uploaded_file:
        doc = Document(uploaded_file)

        nome_empresa = st.text_input("Nome da Empresa")
        nome_fornecedor = st.text_input("Nome do Fornecedor")

        if st.button("Gerar Documento"):
            for para in doc.paragraphs:
                para.text = para.text.replace("{nome_empresa}", nome_empresa)
                para.text = para.text.replace("{nome_fornecedor}", nome_fornecedor)

            output = BytesIO()
            doc.save(output)
            output.seek(0)

            st.download_button(
                label="📥 Baixar Documento Editado",
                data=output,
                file_name="contrato_editado.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

elif page == "sobre":
    # ---- PÁGINA SOBRE ----
    st.title("ℹ️ Sobre o Editor de Contratos")
    st.write("""
    Este sistema foi desenvolvido para tornar a personalização de contratos mais eficiente e intuitiva.

    ### 💡 Recursos Principais:
    - Upload de documentos `.docx`
    - Edição dinâmica dos campos `{nome_empresa}` e `{nome_fornecedor}`
    - Download instantâneo do contrato editado
    - Interface rápida e minimalista inspirada no **Superhuman**
    """)

    st.success("Feito com ❤️ usando Streamlit")
