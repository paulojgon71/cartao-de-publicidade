import requests
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
import io
from PIL import Image

def buscar_logo_por_dominio(url):
    """Tenta obter o logo automaticamente via Clearbit API."""
    try:
        # Extrai o domínio (ex: roady.pt)
        dominio = url.replace("https://", "").replace("http://", "").split("/")[0]
        if dominio.startswith("www."):
            dominio = dominio[4:]
            
        logo_url = f"https://logo.clearbit.com/{dominio}"
        response = requests.get(logo_url, timeout=5)
        
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        return None
    except:
        return None

def gerar_texto_gemini(api_key, nome, setor):
    """Gera o slogan usando o modelo Gemini 1.5 Flash."""
    try:
        # Limpeza de segurança da chave (remove aspas e espaços)
        api_key_limpa = api_key.strip().strip('"').strip("'")
        genai.configure(api_key=api_key_limpa)
        
        # Modelo atualizado (necessita de google-generativeai >= 0.7.2 no requirements.txt)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (f"Escreve um slogan publicitário criativo e muito curto para a empresa {nome} "
                  f"do setor {setor}. Máximo 8 palavras. Não uses aspas nem títulos.")
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Excelência e qualidade para o seu negócio."
            
    except Exception as e:
        # Retorna o erro detalhado para ajudar a diagnosticar no ecrã
        return f"Erro na IA: {str(e)}"

def gerar_pdf(nome, slogan, cor, telefone, morada, logo_pil=None):
    """Cria o PDF profissional com logo, cores da marca e contactos."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((85*mm, 55*mm)))
    
    # --- Design: Barra Superior Colorida ---
    c.setFillColor(cor)
    c.rect(0, 40*
