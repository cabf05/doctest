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

# CSS for a professional navbar and layout
custom_css = """
<style>
/* Navbar fixed at the top */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: #ffffff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 30px;
}

.navbar .logo {
    font-size: 22px;
    font-weight: bold;
    color: #333333;
}

.navbar .menu {
    display: flex;
    gap: 25px;
}

.navbar .menu a {
    text-decoration: none;
    font-size: 16px;
    color: #555555;
    transition: color 0.3s;
}

.navbar .menu a:hover {
    color: #ff4081;
}

/* Content pushed below navbar */
.content {
    margin-top: 80px;
    padding: 20px 30px;
}

/* Custom primary button */
div.stButton > button {
    background-color: #ff4081;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-size: 16px;
    transition: background-color 0.3s, transform 0.2s;
}
div.stButton > button:hover {
    background-color: #e73370;
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

# Initialize current page in session state using st.query_params
if "page" not in st.session_state:
    params = st.query_params
    st.session_state.page = params.get("page", ["home"])[0] if params and "page" in params else "home"

current_page = st.session_state.page

# Navigation callbacks update session state and query params
def go_to_home():
    st.session_state.page = "home"
    st.set_query_params(page="home")

def go_to_editor():
    st.session_state.page = "editor"
    st.set_query_params(page="editor")

def go_to_about():
    st.session_state.page = "about"
    st.set_query_params(page="about")

st.markdown('<div class="content">', unsafe_allow_html=True)

if current_page == "home":
    st.title("Bem-vindo ao Editor de Contratos")
    st.write("Experimente uma experiência minimalista, rápida e profissional para editar seus contratos de forma intuitiva.")
    
    # Display Lottie animation if available
    animation = load_lottiefile("assets/animation.json")
    if animation:
        st_lottie(animation, height=300)
    else:
        st.info("Animação não encontrada.")
    
    st.button("Comece Agora", on_click=go_to_editor)

elif current_page == "editor":
    st.title("Editor de Contrato")
    uploaded_file = st.file_uploader("Faça o upload do arquivo .docx", type="docx")
    
    if uploaded_file:
        doc = Document(uploaded_file)
        
        # Input fields for placeholders
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
                label="Baixar Documento Editado",
                data=output,
                file_name="contrato_editado.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

elif current_page == "about":
    st.title("Sobre o Editor de Contratos")
    st.write("""
    Este sistema foi desenvolvido para facilitar a personalização de contratos de forma rápida e intuitiva.
    
    **Recursos Principais:**
    - Upload de documentos `.docx`
    - Substituição dinâmica de placeholders
    - Download instantâneo do documento editado
    - Interface minimalista e profissional, inspirada no design do Superhuman

    Desenvolvido com Streamlit, python-docx e Streamlit-Lottie.
    """)
    st.info("Feito com ❤️ por sua equipe de desenvolvimento.")
    
st.markdown('</div>', unsafe_allow_html=True)
