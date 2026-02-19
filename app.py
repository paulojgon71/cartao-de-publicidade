import streamlit as st
from engine import buscar_logo_por_dominio, gerar_texto_gemini, gerar_pdf
from PIL import Image

st.set_page_config(page_title="AI AdGen Pro", layout="wide")

st.title("🚀 AI AdGen Pro: Automático & Inteligente")

# Inicializar estado do slogan se não existir
if 'slogan' not in st.session_state:
    st.session_state['slogan'] = ""

with st.sidebar:
    st.header("1. Configuração")
    url = st.text_input("URL da Empresa:", placeholder="ex: roady.pt")
    setor = st.selectbox("Setor:", ["Automóvel", "Tecnologia", "Restauração", "Saúde"])
    cor_marca = st.color_picker("Cor do Anúncio:", "#E30613")
    
    st.header("2. Contactos")
    telefone = st.text_input("Telefone:", "243 000 000")
    morada = st.text_input("Morada:", "Santarém, Portugal")
    
    st.header("3. Logótipo")
    # Tenta buscar automático se houver URL
    logo_auto = None
    if url:
        logo_auto = buscar_logo_por_dominio(url)
        if logo_auto:
            st.success("✅ Logo encontrado automaticamente!")
            st.image(logo_auto, width=100)
    
    logo_manual = st.file_uploader("Ou carregar manual (PNG/JPG):", type=["png", "jpg"])

# Lógica Principal
if url:
    nome_empresa = url.split(".")[1].capitalize() if "." in url else "Empresa"
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ Gerar Slogan com Gemini IA"):
            st.session_state['slogan'] = gerar_texto_gemini(st.secrets["GEMINI_API_KEY"], nome_empresa, setor)
        
        slogan_final = st.text_area("Slogan:", value=st.session_state['slogan'])

    with col2:
        st.subheader("🛠️ Finalizar Anúncio")
        # Decide qual logo usar: manual tem prioridade, se não, usa o automático
        logo_final = Image.open(logo_manual) if logo_manual else logo_auto
        
        if st.button("Gerar PDF Final"):
            pdf = gerar_pdf(nome_empresa, slogan_final, cor_marca, telefone, morada, logo_final)
            st.download_button("📥 Descarregar para Impressão", data=pdf, file_name=f"anuncio_{nome_empresa}.pdf")
else:
    st.info("Insira um URL na barra lateral para começar.")
