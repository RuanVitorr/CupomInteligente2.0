from pathlib import Path

# Conteúdo do README.md
readme_content = """
# 🧾 Cupom Inteligente - Chatbot Fiscal da Paraíba

**Cupom Inteligente** é uma aplicação que utiliza inteligência artificial para ajudar cidadãos a entenderem os componentes de um cupom fiscal, com foco nos impostos cobrados no estado da Paraíba (PB), como o ICMS. A proposta é promover **educação fiscal acessível e automatizada**, através de uma interface de chatbot simples e intuitiva.

## 🚀 Funcionalidades

- 🤖 Chatbot com IA especializada em cupons fiscais da PB.
- 📄 Respostas claras sobre impostos como ICMS, NFC-e, alíquotas, obrigatoriedade e base de cálculo.
- 🧠 Sistema multi-agente (usando CrewAI) para gerar, analisar e melhorar as respostas.
- 🖥️ Interface web via Streamlit.
- 📈 Ideal para cidadãos, professores, estudantes ou pequenos empreendedores.

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Langchain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/) (necessário configurar chave de API)

## ⚙️ Instalação

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/cupom-inteligente.git
cd cupom-inteligente
