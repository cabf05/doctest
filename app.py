import streamlit as st
from docx import Document
from io import BytesIO
from streamlit_lottie import st_lottie
import json

# Set page configuration
st.set_page_config(page_title="Editor de Contrato", page_icon="✍️", layout="wide")

def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return None

# Custom CSS for a minimalistic design using white, black, and gray
custom_css = """
<style>
    body {
        background-color: #fff;
        font-family: 'Helvetica Neue', sans-serif;
        color: #000;
    }
    /* Navbar styling */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: #fff;
        border-bottom: 1px solid #ccc;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 30px;
        z-index: 1000;
    }
    .navbar .logo {
        font-size: 24px;
        font-weight: bold;
        color: #000;
    }
    .navbar .menu {
        display: flex;
        gap: 20px;
    }
    .navbar .menu a {
        text-decoration: none;
        font-size: 16px;
        color: #000;
        transition: color 0.3s ease;
    }
    .navbar .menu a:hover {
        color: #888;
    }
    /* Main content area: push below navbar */
    .content {
        margin-top: 80px;
        padding: 40px 30px;
    }
    /* Custom button styling */
    div.stButton > button {
        background-color: #000;
        color: #fff;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        font-size: 16px;
        transition: background-color 0.3s, transform 0.2s;
    }
    div.stButton > button:hover {
        background-color: #444;
        transform: scale(1.02);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Navbar HTML
nav_bar = """
<div class="navbar">
    <div class="logo">Editor de Contrato</div>
    <div class="menu">
        <a href="/?page=home">Home</a>
        <a href="/?page=editor">Editor</a>
        <a href="/?page=about">Sobre</a>
    </div>
</div>
"""
st.markdown(nav_bar, unsafe_allow_html=True)

# Initialize current page using session_state and st.query_params
if "page" not in st.session_state:
    params = st.query_params
    st.session_state.page = params.get("page", ["home"])[0] if params and "page" in params else "home"

current_page = st.session_state.page

# Navigation callback functions that update the session state and query params
def go_to_home():
    st.session_state.page = "home"
    st.query_params = {"page": "home"}

def go_to_editor():
    st.session_state.page = "editor"
    st.query_params = {"page": "editor"}

def go_to_about():
    st.session_state.page = "about"
    st.query_params = {"page": "about"}

st.markdown('<div class="content">', unsafe_allow_html=True)

if current_page == "home":
    # Home page (Landing Page)
    st.title("Bem-vindo ao Editor de Contratos")
    st.write("Experimente uma interface minimalista e profissional para editar seus contratos com agilidade.")
    
    # Display Lottie animation if available
    animation = load_lottiefile("assets/animation.json")
    if animation:
        st_lottie(animation, height=300)
    else:
        st.info("Animação não encontrada.")
    
    st.button("Comece Agora", on_click=go_to_editor)

elif current_page == "editor":
    # Editor page
    st.title("Editor de Contrato")
    uploaded_file = st.file_uploader("Faça o upload do arquivo .docx", type="docx")
    
    if uploaded_file:
        doc = Document(uploaded_file)
        
        # Input fields for placeholders
        nome_empresa = st.text_input("Nome da Empresa")
        nome_fornecedor = st.text_input("Nome do Fornecedor")
        
        if st.button("Gerar Documento"):
            # Replace placeholders with provided text
            for para in doc.paragraphs:
                para.text = para.text.replace("{nome_empresa}", nome_empresa)
                para.text = para.text.replace("{nome_fornecedor}", nome_fornecedor)
            
            # Save the modified document to memory
            output = BytesIO()
            doc.save(output)
            output.seek(0)
            
            st.download_button(
                label="Baixar Documento Editado",
                data=output,
                file_name="contrato_editado.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

elif current_page == "about":
    # About page
    st.title("Sobre o Editor de Contratos")
    st.write("""
    Este sistema foi desenvolvido para simplificar a personalização de contratos de forma rápida e intuitiva.
    
    **Recursos Principais:**
    - Upload de documentos `.docx`
    - Substituição dinâmica de placeholders
    - Download instantâneo do documento editado
    - Interface minimalista com foco em usabilidade e clareza

    Desenvolvido com Streamlit, python-docx e Streamlit-Lottie.
    """)
    st.info("Feito com ❤️ por sua equipe de desenvolvimento.")
    
st.markdown('</div>', unsafe_allow_html=True)
