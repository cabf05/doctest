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
    except Exception:
        return None

# Estilização com CSS para um layout premium
custom_css = """
<style>
    body {
        background-color: #fff;
        font-family: 'Helvetica Neue', sans-serif;
        color: #000;
    }
    /* Barra Superior Customizada */
    .top-bar {
        background-color: #fff;
        border-bottom: 1px solid #ccc;
        padding: 10px 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #000;
        margin-bottom: 20px;
    }
    /* Estilo dos botões */
    .stButton > button {
        background-color: #000;
        color: #fff;
        border-radius: 4px;
        font-size: 16px;
        transition: background 0.3s ease, transform 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #444;
        transform: scale(1.02);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---- 🚀 Criando a Barra Superior ----
st.markdown('<div class="top-bar">Editor de Contrato</div>', unsafe_allow_html=True)

# ---- 🚀 Criando a Barra Lateral para Navegação ----
st.sidebar.title("📂 Menu")
page = st.sidebar.radio("Navegação", ["🏠 Home", "✍️ Editor", "ℹ️ Sobre"])

# ---- ✨ Renderizando Páginas ----
if page == "🏠 Home":
    st.title("Bem-vindo ao Editor de Contratos")
    st.write("Experimente uma experiência minimalista e profissional para editar seus contratos.")

    # Exibir animação Lottie se disponível
    animation = load_lottiefile("assets/animation.json")
    if animation:
        st_lottie(animation, height=300)
    else:
        st.info("Animação não encontrada.")

    st.button("Ir para o Editor", on_click=lambda: st.experimental_set_query_params(page="Editor"))

elif page == "✍️ Editor":
    st.title("Editor de Contrato")
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
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

elif page == "ℹ️ Sobre":
    st.title("Sobre o Editor de Contratos")
    st.write("""
    Este sistema foi desenvolvido para facilitar a personalização de contratos de forma rápida e intuitiva.

    **📌 Recursos Principais:**
    - Upload de documentos `.docx`
    - Substituição dinâmica de placeholders `{nome_empresa}` e `{nome_fornecedor}`
    - Download instantâneo do documento editado
    - Interface minimalista, inspirada no design do Superhuman

    🔥 **Feito com Streamlit, python-docx e Streamlit-Lottie.**
    """)
    st.success("💡 Feito com ❤️ para melhorar sua produtividade.")

