import requests
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
import io
from PIL import Image

def buscar_logo_por_dominio(url):
    try:
        dominio = url.replace("https://", "").replace("http://", "").split("/")[0]
        if dominio.startswith("www."): dominio = dominio[4:]
        logo_url = f"https://logo.clearbit.com/{dominio}"
        response = requests.get(logo_url, timeout=5)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        return None
    except:
        return None

def gerar_texto_gemini(api_key, nome, setor):
    try:
        # 1. Limpeza da chave
        api_key_limpa = api_key.strip().strip('"').strip("'")
        genai.configure(api_key=api_key_limpa)
        
        # 2. Especificar o modelo com o prefixo completo 'models/' 
        # Isto evita que a biblioteca tente caminhos beta errados
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = f"Escreve um slogan publicitário curto para a empresa {nome} do setor {setor}. Máximo 8 palavras."
        
        # 3. Gerar conteúdo
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        return "Qualidade e confiança para o seu veículo."
            
    except Exception as e:
        # Se o 1.5-flash falhar, tentamos o 1.0-pro como última alternativa
        try:
            model_backup = genai.GenerativeModel('models/gemini-1.0-pro')
            response = model_backup.generate_content(f"Slogan para {nome}")
            return response.text.strip()
        except:
            return f"Erro Crítico: {str(e)}"

def gerar_pdf(nome, slogan, cor, telefone, morada, logo_pil=None):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((85*mm, 55*mm)))
    
    # Barra Superior
    c.setFillColor(cor)
    c.rect(0, 40*mm, 85*mm, 15*mm, fill=1, stroke=0)
    
    # Nome
    c.setFillColor("#FFFFFF")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(5*mm, 46*mm, nome.upper())
    
    if logo_pil:
        try:
            img_buffer = io.BytesIO()
            logo_pil.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            c.drawImage(io.BytesIO(img_buffer.read()), 62*mm, 42*mm, width=16*mm, preserveAspectRatio=True, mask='auto')
        except: pass 

    # Slogan
    c.setFillColor("#333333")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5*mm, 30*mm, slogan[:60])
    
    # Rodapé
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
