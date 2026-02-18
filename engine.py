import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
import io

def extrair_dados_site(url):
    try:
        if not url.startswith("http"): url = "https://" + url
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
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

def gerar_texto_gemini(api_key, nome, setor):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Cria um slogan publicitário curto para a empresa {nome} do setor {setor}. Máximo 12 palavras."
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Excelência e Confiança em cada detalhe."

def gerar_pdf(nome, slogan, cor):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((85*mm, 55*mm)))
    c.setStrokeColor(cor)
    c.rect(1*mm, 1*mm, 83*mm, 53*mm)
    c.setFillColor(cor)
    c.rect(1*mm, 40*mm, 83*mm, 14*mm, fill=1)
    c.setFillColor("#FFFFFF")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(5*mm, 46*mm, nome.upper())
    c.setFillColor("#333333")
    c.setFont("Helvetica", 10)
    c.drawString(5*mm, 30*mm, slogan)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
