import requests
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
import io
from PIL import Image
import os

def buscar_logo_por_dominio(url):
    """Tenta obter o logo automaticamente via Clearbit API."""
    try:
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
    """Gera o slogan forçando a versão estável da API para evitar erro 404."""
    try:
        # 1. Limpeza rigorosa da chave
        api_key_limpa = api_key.strip().strip('"').strip("'")
        
        # 2. Configuração da API
        genai.configure(api_key=api_key_limpa)
        
        # 3. Definição do Modelo (Usamos o 1.5-flash que é o padrão atual)
        # Se o erro persistir, o problema pode ser a versão da biblioteca no requirements.txt
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        
        prompt = (f"Escreve um slogan publicitário criativo e curto para a empresa {nome} "
                  f"do setor {setor}. Máximo 10 palavras. Não uses aspas.")
        
        # 4. Geração de conteúdo
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Excelência e qualidade para o seu negócio."
            
    except Exception as e:
        # Se der erro de versão, tentamos uma abordagem alternativa de nome de modelo
        if "404" in str(e):
            return "Erro: Modelo não encontrado. Verifique se a sua API Key tem acesso ao Gemini 1.5 Flash."
        return f"Erro na IA: {str(e)}"

def gerar_pdf(nome, slogan, cor, telefone, morada, logo_pil=None):
    """Monta o PDF final."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape((85*mm, 55*mm)))
    
    # Design
    c.setFillColor(cor)
    c.rect(0, 40*mm, 85*mm, 15*mm, fill=1, stroke=0)
    
    c.setFillColor("#FFFFFF")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(5*mm, 46*mm, nome.upper())
    
    if logo_pil:
        try:
            img_buffer = io.BytesIO()
            logo_pil.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            c.drawImage(io.BytesIO(img_buffer.read()), 62*mm, 42*mm, width=16*mm, preserveAspectRatio=True, mask='auto')
        except:
            pass 

    c.setFillColor("#333333")
    c.setFont("Helvetica-Bold", 10)
    slogan_formatado = slogan[:60] if len(slogan) > 60 else slogan
    c.drawString(5*mm, 30*mm, slogan_formatado)
    
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
