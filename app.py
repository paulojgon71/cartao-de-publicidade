import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
import qrcode
import io
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AI AdGen Pro - Gemini Edition", page_icon="🚀", layout="wide")

# --- FUNÇÕES DE LÓGICA (O Cérebro) ---

def extrair_dados_site(url):
    """Extrai o nome provável e o logótipo de um site."""
    try:
        if not url.startswith("http"): url = "https://" + url
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Tenta encontrar o logo em meta tags ou imagens
        logo_url = None
        meta_logo = soup.find("meta", property="og:image")
        if meta_logo:
            logo_url = meta_logo["content"]
        else:
            for img in soup.find_all("img"):
                if "logo" in img.get("src", "").lower():
                    logo_url = urljoin(url, img.get("src"))
                    break
        
        nome_empresa = url.split(".")[1].capitalize() if "." in url else "Empresa"
        return nome_empresa, logo_url
    except:
        return "Empresa", None

def gerar_texto_gemini(nome, setor):
    """Usa a API do Gemini para criar um slogan publicitário."""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Cria um slogan publicitário curto (máx 12 palavras) para a empresa {nome} do setor {setor}. O tom deve ser profissional e focado em atrair clientes para uma revista. Responde apenas com a frase."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Excelência e Confiança em cada detalhe para o seu negócio."

def gerar_pdf(nome, slogan, cor, logo_url):
    """Gera um ficheiro PDF em alta resolução pronto para impressão."""
    buffer = io.BytesIO()
    # Tamanho aproximado de um cartão de visita/anúncio pequeno (85x55mm)
    c = canvas.Canvas(buffer, pagesize=landscape((85*mm, 55*mm)))
    
    # Desenhar moldura e design
    c.setStrokeColor(cor)
    c.setLineWidth(1*mm)
    c.rect(1*mm, 1*mm, 83*mm, 53*mm)
    
    # Cabeçalho Colorido
    c.setFillColor(cor)
    c.rect(1*mm, 40*mm, 83*mm, 14*mm, fill=1)
    
    # Nome da Empresa
    c.setFillColor("#FFFFFF")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(5*mm, 46*mm, nome.upper())
    
    # Slogan (com quebra de linha se necessário)
    c.setFillColor("#333333")
    c.setFont("Helvetica", 10)
    text_obj = c.beginText(5*mm, 30*mm)
    text_obj.textLines(slogan)
    c.drawText(text_obj)
    
    # Nota de rodapé
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor("#999999")
    c.drawString(5*mm, 4*mm, "Publicidade Profissional | Gerado por AI AdGen")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- INTERFACE DO UTILIZADOR (Streamlit) ---

st.title("🚀 AI AdGen Pro: De URL a Anúncio")
st.markdown("Insira o link do site e deixe a Inteligência Artificial do Google Gemini criar o seu anúncio de revista.")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    url = st.text_input("URL do Site:", placeholder="www.roady.pt")
    setor = st.selectbox("Setor do Negócio:", ["Automóvel", "Tecnologia", "Restauração", "Saúde", "Imobiliário"])
    cor_marca = st.color_picker("Cor Principal:", "#003399")
    st.divider()
    st.info("Certifica-te que configuraste a 'GEMINI_API_KEY' nos Secrets do Streamlit.")

# Lógica Principal
if url:
    nome_est, logo_est = extrair_dados_site(url)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Conteúdo do Anúncio")
        nome_final = st.text_input("Nome da Empresa:", value=nome_est)
        
        if st.button("✨ Gerar Slogan com Gemini IA"):
            with st.spinner("O Gemini está a escrever..."):
                st.session_state['slogan_gerado'] = gerar_texto_gemini(nome_final, setor)
        
        slogan_final = st.text_area("Slogan do Anúncio:", value=st.session_state.get('slogan_gerado', "A sua melhor escolha em serviços."))

    with col2:
        st.subheader("🖼️ Pré-visualização")
        # Simulação visual do cartão usando HTML/CSS
        st.markdown(f"""
        <div style="border: 4px solid {cor_marca}; padding: 25px; border-radius: 10px; background-color: white; min-height: 200px;">
            <div style="background-color: {cor_marca}; margin: -25px -25px 20px -25px; padding: 15px; border-radius: 5px 5px 0 0;">
                <h2 style="color: white; margin: 0; font-family: sans-serif;">{nome_final.upper()}</h2>
            </div>
            <p style="color: #333; font-size: 20px; font-weight: bold; font-family: sans-serif;">{slogan_final}</p>
            <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px; font-size: 12px; color: #999;">
                📍 Pronto para Revista | 📞 Contacto no Verso
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Botão de Exportação
    st.divider()
    if st.button("🛠️ Preparar PDF para Impressão"):
        pdf = gerar_pdf(nome_final, slogan_final, cor_marca, logo_est)
        st.download_button(
            label="📥 Descarregar Anúncio em Alta Resolução",
            data=pdf,
            file_name=f"anuncio_{nome_final.lower()}.pdf",
            mime="application/pdf"
        )
else:
    st.warning("Aguardando URL para começar...")
