# 🚀 AI AdGen Pro: De URL a Anúncio com Google Gemini

O **AI AdGen Pro** é uma solução de automação de marketing que transforma a presença digital de uma empresa (URL) num anúncio impresso profissional para revistas em poucos segundos.

## 🧠 Arquitetura do Projeto
O projeto foi desenhado seguindo princípios de **separação de responsabilidades (SoC)**, dividindo a aplicação em dois módulos principais:

* **`app.py`**: Camada de interface (Frontend) desenvolvida em Streamlit. Gere a interação com o utilizador, recolha de inputs e renderização visual.
* **`engine.py`**: Motor de lógica (Backend). Responsável pelo Web Scraping, integração com a API generativa do Google Gemini e processamento de ficheiros PDF.



## ✨ Funcionalidades Principais
- **Web Scraping Inteligente:** Identifica automaticamente a identidade visual e logótipos através da análise do código HTML do site.
- **Copywriting por IA:** Integração com o modelo `gemini-1.5-flash` para criar slogans publicitários de alto impacto.
- **Gerador de PDF Vectorial:** Exporta anúncios em formato PDF de alta resolução, garantindo nitidez para impressão gráfica.
- **Design Dinâmico:** Customização de cores e textos em tempo real através da sidebar intuitiva.

## 🛠️ Como Instalar e Usar

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/teu-utilizador/ai-adgen-pro.git](https://github.com/teu-utilizador/ai-adgen-pro.git)
   cd ai-adgen-pro
