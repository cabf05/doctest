import streamlit as st
from docx import Document
from io import BytesIO

# Adicionando CSS personalizado
st.markdown("""
    <style>
    /* Reset básico */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: 'Helvetica Neue', Arial, sans-serif;
      background-color: #fff;
      color: #000;
      line-height: 1.6;
    }
    a {
      text-decoration: none;
      color: inherit;
    }
    /* Navbar fixa no topo */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 60px;
      background: #fff;
      border-bottom: 1px solid #ddd;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 30px;
      z-index: 1000;
    }
    .navbar .logo {
      font-size: 24px;
      font-weight: bold;
    }
    .navbar nav {
      display: flex;
      gap: 20px;
    }
    .navbar nav a {
      font-size: 16px;
      transition: color 0.3s ease;
    }
    .navbar nav a:hover {
      color: #888;
    }
    /* Espaço para que o conteúdo não fique atrás da navbar */
    .content {
      margin-top: 80px;
      padding: 40px 30px;
    }
    /* Seção Hero com animação de fundo */
    .hero {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 80vh;
      background: #f7f7f7;
      overflow: hidden;
      text-align: center;
      padding: 20px;
    }
    .hero h1 {
      font-size: 48px;
      margin-bottom: 20px;
    }
    .hero p {
      font-size: 20px;
      max-width: 600px;
      margin-bottom: 40px;
    }
    .hero .cta-button {
      padding: 15px 30px;
      font-size: 18px;
      background-color: #000;
      color: #fff;
      border: none;
      border-radius: 30px;
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .hero .cta-button:hover {
      background-color: #333;
      transform: scale(1.05);
    }
    /* Animação de fundo sutil */
    .background-animation {
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle at center, #ddd, transparent 70%);
      animation: rotate 20s linear infinite;
      opacity: 0.3;
      z-index: -1;
    }
    @keyframes rotate {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    /* Seção de recursos */
    .features {
      padding: 80px 20px;
      background: #fff;
    }
    .feature {
      max-width: 800px;
      margin: 0 auto 60px auto;
      text-align: center;
    }
    .feature h2 {
      font-size: 32px;
      margin-bottom: 10px;
    }
    .feature p {
      font-size: 18px;
      color: #666;
    }
    /* Seção de contato */
    .contact {
      padding: 80px 20px;
      background: #f7f7f7;
      text-align: center;
    }
    .contact h2 {
      font-size: 32px;
      margin-bottom: 20px;
    }
    .contact p {
      font-size: 18px;
      color: #666;
    }
    .back-button {
      padding: 10px 20px;
      font-size: 16px;
      background-color: #000;
      color: #fff;
      border: none;
      border-radius: 30px;
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.3s ease;
      margin-top: 20px;
    }
    .back-button:hover {
      background-color: #333;
      transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Verifica a página atual com base na query string
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Home"])[0]

if page == "Home":
    # Navbar
    st.markdown("""
        <header class="navbar">
          <div class="logo">PremiumApp</div>
          <nav>
            <a href="#home">Home</a>
            <a href="#features">Recursos</a>
            <a href="#contact">Contato</a>
          </nav>
        </header>
        """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <section class="hero" id="home">
          <div class="background-animation"></div>
          <h1>Bem-vindo ao PremiumApp</h1>
          <p>Uma experiência minimalista e intuitiva com design premium e animações elegantes para otimizar sua produtividade.</p>
          <a href="?page=Editor%20de%20Contrato" class="cta-button">Comece Agora</a>
        </section>
        """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <section class="features" id="features">
          <div class="feature">
            <h2>Design Minimalista</h2>
            <p>Interface limpa e organizada que prioriza a simplicidade e a clareza, eliminando distrações.</p>
          </div>
          <div class="feature">
            <h2>Experiência Intuitiva</h2>
            <p>Navegue de forma simples e eficiente com uma estrutura pensada para a melhor usabilidade.</p>
          </div>
          <div class="feature">
            <h2>Animações Elegantes</h2>
            <p>Transições suaves e efeitos animados que agregam dinamismo sem comprometer a simplicidade.</p>
          </div>
        </section>
        """, unsafe_allow_html=True)

    # Contact Section
    st.markdown("""
        <section class="contact" id="contact">
          <h2>Contato</h2>
          <p>Entre em contato para saber mais sobre nossas soluções premium.</p>
        </section>
        """, unsafe_allow_html=True)

elif page == "Editor de Contrato":
    st.markdown("<div class='content'>", unsafe_allow_html=True)

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

    st.markdown('<a href="?page=Home" class="back-button">Voltar para Home</a>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
