import streamlit as st
from docx import Document
from io import BytesIO
import base64
from pathlib import Path
import time

# Configurações da página
st.set_page_config(
    page_title="Editor de Contrato Premium",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    /* Cores e tema */
    :root {
        --primary-color: #4F46E5;
        --secondary-color: #9333EA;
        --text-color: #1E293B;
        --bg-color: #F8FAFC;
        --card-bg: #FFFFFF;
        --accent: #6366F1;
    }
    
    /* Estilo de fundo e corpo */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    /* Estilo dos cards */
    .css-1r6slb0, .css-keje6w {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
    
    /* Estilo dos botões */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
    }
    
    /* Estilo para upload de arquivo */
    .uploadedFile {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px dashed var(--primary-color);
    }
    
    /* Estilos para inputs */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    
    /* Título personalizado */
    .custom-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Separador */
    .separator {
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: 2px;
        margin: 1rem 0;
        width: 100%;
    }
    
    /* Ícone de sucesso */
    .success-icon {
        font-size: 3rem;
        color: #10B981;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Container para os cartões */
    .card-container {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
    }
    
    /* Estilo para o passo a passo */
    .step {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .step-number {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-weight: bold;
    }
    
    /* Animação de loading */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Função para mostrar animação de carregamento
def loading_animation():
    with st.spinner("Processando..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        st.success("Concluído!")
        time.sleep(0.5)
        return True

# Função para adicionar ícone
def add_icon(icon_name):
    st.markdown(f'<div class="success-icon">{icon_name}</div>', unsafe_allow_html=True)

# Título personalizado
st.markdown('<h1 class="custom-title">Editor de Contrato Premium</h1>', unsafe_allow_html=True)

# Inicializar estado da sessão
if 'stage' not in st.session_state:
    st.session_state.stage = 1

# Container principal
with st.container():
    # Estágio 1: Upload de arquivo
    if st.session_state.stage == 1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("📁 Upload de Documento")
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # Instruções
        st.markdown("Faça o upload do seu modelo de contrato DOCX contendo os marcadores `{nome_empresa}` e `{nome_fornecedor}`.")
        
        # Área de upload com estilo personalizado
        uploaded_file = st.file_uploader("", type="docx", key="docx_uploader")
        
        # Verificar se o arquivo foi carregado
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.success("Arquivo carregado com sucesso!")
            
            # Mostrar detalhes do arquivo
            file_details = {
                "Nome do arquivo": uploaded_file.name,
                "Tipo de arquivo": uploaded_file.type,
                "Tamanho": f"{uploaded_file.size / 1024:.2f} KB"
            }
            
            # Exibir detalhes em uma tabela estilizada
            st.markdown("### Detalhes do arquivo")
            for key, value in file_details.items():
                st.markdown(f"**{key}:** {value}")
            
            # Botão para avançar para o próximo estágio
            if st.button("Continuar para edição"):
                st.session_state.doc = Document(uploaded_file)
                st.session_state.stage = 2
                st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Mostrar dicas de uso
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("💡 Como usar")
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # Passo a passo
        st.markdown('<div class="step"><div class="step-number">1</div><div>Faça upload do seu modelo de contrato (formato DOCX)</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="step"><div class="step-number">2</div><div>Preencha os campos com as informações necessárias</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="step"><div class="step-number">3</div><div>Gere e baixe seu contrato personalizado</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Estágio 2: Edição de campos
    elif st.session_state.stage == 2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("✏️ Edição de Contrato")
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # Formulário para edição
        with st.form(key="edit_form"):
            col1, col2 = st.columns(2)
            with col1:
                nome_empresa = st.text_input("Nome da Empresa", key="empresa")
            with col2:
                nome_fornecedor = st.text_input("Nome do Fornecedor", key="fornecedor")
            
            # Exibir o nome do arquivo carregado
            st.markdown(f"**Arquivo:** {st.session_state.uploaded_file.name}")
            
            # Botões para ações
            col1, col2 = st.columns(2)
            with col1:
                back_button = st.form_submit_button("⬅️ Voltar")
            with col2:
                submit_button = st.form_submit_button("✨ Gerar Documento")
            
            if back_button:
                st.session_state.stage = 1
                st.experimental_rerun()
            
            if submit_button:
                if nome_empresa and nome_fornecedor:
                    # Substituição dos placeholders
                    doc = st.session_state.doc
                    for para in doc.paragraphs:
                        if "{nome_empresa}" in para.text:
                            para.text = para.text.replace("{nome_empresa}", nome_empresa)
                        if "{nome_fornecedor}" in para.text:
                            para.text = para.text.replace("{nome_fornecedor}", nome_fornecedor)
                    
                    # Criar um novo arquivo .docx em memória
                    output = BytesIO()
                    doc.save(output)
                    output.seek(0)
                    
                    # Guardar no estado da sessão
                    st.session_state.output = output
                    st.session_state.nome_empresa = nome_empresa
                    st.session_state.nome_fornecedor = nome_fornecedor
                    st.session_state.stage = 3
                    st.experimental_rerun()
                else:
                    st.warning("Por favor, preencha todos os campos.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Preview (simulado)
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("👁️ Preview")
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.info("As alterações serão aplicadas no documento final. Esta é uma representação visual.")
        
        # Simulação de preview do documento
        preview_text = """
        **CONTRATO DE PRESTAÇÃO DE SERVIÇOS**
        
        **CONTRATANTE:** {nome_empresa}
        **FORNECEDOR:** {nome_fornecedor}
        
        **CLÁUSULA PRIMEIRA - DO OBJETO**
        O presente contrato tem como objeto a prestação de serviços...
        """
        
        # Substituir placeholders no preview
        preview_text = preview_text.replace("{nome_empresa}", nome_empresa if nome_empresa else "[Nome da Empresa]")
        preview_text = preview_text.replace("{nome_fornecedor}", nome_fornecedor if nome_fornecedor else "[Nome do Fornecedor]")
        
        st.markdown(preview_text)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Estágio 3: Download
    elif st.session_state.stage == 3:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("🎉 Documento Gerado")
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # Mostrar animação de sucesso
        add_icon("✅")
        
        # Mostrar os dados usados
        st.markdown("### Detalhes do documento gerado")
        st.markdown(f"**Nome da Empresa:** {st.session_state.nome_empresa}")
        st.markdown(f"**Nome do Fornecedor:** {st.session_state.nome_fornecedor}")
        
        # Botão de download estilizado
        output_filename = f"contrato_{st.session_state.nome_empresa.lower().replace(' ', '_')}.docx"
        
        st.download_button(
            label="📥 Baixar Documento Modificado",
            data=st.session_state.output,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        
        # Opções adicionais
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Editar Novamente"):
                st.session_state.stage = 2
                st.experimental_rerun()
        with col2:
            if st.button("📁 Novo Documento"):
                st.session_state.stage = 1
                st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feedback
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("💬 Feedback")
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.markdown("Seu documento foi gerado com sucesso. Como foi sua experiência?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("😀 Excelente")
        with col2:
            st.button("🙂 Boa")
        with col3:
            st.button("😐 Regular")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #94A3B8; font-size: 0.8rem;">
    © 2025 Editor de Contrato Premium • Criado com ❤️
</div>
""", unsafe_allow_html=True)
