import streamlit as st
from engine import extrair_dados_site, gerar_texto_gemini, gerar_pdf

st.set_page_config(page_title="AI AdGen Pro", layout="wide")

st.title("🚀 AI AdGen Pro")

# Sidebar
with st.sidebar:
    url = st.text_input("URL do Site:")
    setor = st.selectbox("Setor:", ["Automóvel", "Tecnologia", "Saúde"])
    cor_marca = st.color_picker("Cor:", "#003399")

if url:
    nome_est, _ = extrair_dados_site(url)
    nome = st.text_input("Nome da Empresa:", value=nome_est)
    
    if st.button("✨ Gerar com Gemini"):
        st.session_state['slogan'] = gerar_texto_gemini(st.secrets["GEMINI_API_KEY"], nome, setor)
    
    slogan = st.text_area("Slogan:", value=st.session_state.get('slogan', ""))

    if st.button("🛠️ Gerar PDF"):
        pdf = gerar_pdf(nome, slogan, cor_marca)
        st.download_button("📥 Descarregar Anúncio", data=pdf, file_name="anuncio.pdf")
