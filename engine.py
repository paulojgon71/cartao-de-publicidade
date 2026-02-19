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
        # Limpa o URL para extrair apenas o domínio
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
    """Usa o Gemini para criar o slogan com tratamento de erros rigoroso."""
    try:
        # Limpeza de segurança: remove aspas ou espaços que venham do TOML
        api_key_limpa = api_key.strip().strip('"').strip("'")
        
        genai.configure(api_key=api_key_limpa)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Escreve um slogan publicitário criativo e curto para a empresa {nome} do setor {setor}. Máximo 10 palavras. Não uses aspas nem prefixos."
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Excelência e qualidade para o seu negócio."
            
    except Exception as e:
        # Se falhar, retorna o erro real para sabermos o que corrigir nos Secrets
        return f"Erro na IA: {str(e)}"

def gerar_pdf(nome, slogan, cor, telefone, morada, logo_pil=None):
    """Monta o PDF final com os dados e o logo em alta resolução."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((85*mm, 55*mm)))
    
    # --- Background e Design ---
    c.setFillColor(cor)
    c.rect(0, 40*mm, 85*mm, 15*mm, fill=1, stroke=0)
    
    # --- Nome da Empresa ---
    c.setFillColor("#FFFFFF")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(5*mm, 46*mm, nome.upper())
    
    # --- Inserção do Logótipo ---
    if logo_pil:
        try:
            img_buffer = io.BytesIO()
            logo_pil.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            # Posicionamento no canto superior direito
            c.drawImage(io.BytesIO(img_buffer.read()), 62*mm, 42*mm, width=16*mm, preserveAspectRatio=True, mask='auto')
        except:
            pass # Se a imagem falhar, o PDF continua sem o logo

    # --- Texto do Slogan ---
    c.setFillColor("#333333")
    c.setFont("Helvetica-Bold", 10)
    # Garante que o texto não sai da página
    slogan_curto = slogan[:60] if len(slogan) > 60 else slogan
    c.drawString(5*mm, 30*mm, slogan_curto)
    
    # --- Contactos e Rodapé ---
    c.setFillColor(cor)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(5*mm, 12*mm, f"TEL: {telefone}")
    
    c.setFillColor("#666666")
    c.setFont("Helvetica", 8)
    c.drawString(5*mm, 7*mm, f"LOC: {morada}")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
