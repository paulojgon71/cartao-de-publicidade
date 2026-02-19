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
        api_key_limpa = api_key.strip().strip('"').strip("'")
        genai.configure(api_key=api_key_limpa)
        
        # Tentativa 1: Modelo Flash (Mais rápido)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Slogan curto para {nome} ({setor}). Máximo 8 palavras.")
            return response.text.strip()
        except:
            # Tentativa 2: Modelo Pro (Caso o Flash não seja encontrado)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Slogan curto para {nome} ({setor}). Máximo 8 palavras.")
            return response.text.strip()
            
    except Exception as e:
        import google.generativeai as v
        return f"Erro: {str(e)} | Lib Version: {v.__version__}"

def gerar_pdf(nome, slogan, cor, telefone, morada, logo_pil=None):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((85*mm, 55*mm)))
    c.setFillColor(cor); c.rect(0, 40*mm, 85*mm, 15*mm, fill=1, stroke=0)
    c.setFillColor("#FFFFFF"); c.setFont("Helvetica-Bold", 14); c.drawString(5*mm, 46*mm, nome.upper())
    
    if logo_pil:
        try:
            img_buffer = io.BytesIO(); logo_pil.save(img_buffer, format='PNG'); img_buffer.seek(0)
            c.drawImage(io.BytesIO(img_buffer.read()), 62*mm, 42*mm, width=16*mm, preserveAspectRatio=True, mask='auto')
        except: pass 

    c.setFillColor("#333333"); c.setFont("Helvetica-Bold", 10)
    c.drawString(5*mm, 30*mm, slogan[:60])
    c.setFillColor(cor); c.setFont("Helvetica-Bold", 9); c.drawString(5*mm, 12*mm, f"TEL: {telefone}")
    c.setFillColor("#666666"); c.setFont("Helvetica", 8); c.drawString(5*mm, 7*mm, f"LOC: {morada}")
    c.showPage(); c.save(); buffer.seek(0)
    return buffer
