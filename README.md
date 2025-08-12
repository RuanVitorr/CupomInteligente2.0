# 🧾 Cupom Inteligente — Chatbot Fiscal da Paraíba

**Cupom Inteligente** é uma aplicação com inteligência artificial que ajuda o cidadão a entender o que diabos tem naquele cupom fiscal — especialmente os impostos da Paraíba, tipo ICMS.  
O objetivo? Educação fiscal simples, direta e sem enrolação, via chatbot.

---

## 🚀 Funcionalidades

- 🤖 Chatbot com IA especializado em cupons fiscais da PB  
- 📄 Explicações claras sobre ICMS, NFC-e, alíquotas, base de cálculo e obrigatoriedade  
- 🧠 Arquitetura multi-agente (CrewAI) que gera, analisa e melhora respostas  
- 🌐 Backend com FastAPI na rota `/perguntar`  
- 💬 Frontend em Vue.js, chat responsivo pra PC e celular  
- 📱 Acesso local pela mesma rede Wi-Fi, sem complicação

---

## 🛠 Tecnologias

**Backend**  
- Python 3.10+  
- FastAPI + Uvicorn  
- CrewAI  
- LangChain  
- OpenAI API (ou Google Gemini, opcional)  
- python-dotenv  

**Frontend**  
- Vue 3 (Vite)  
- TypeScript (opcional)  
- fetch / axios  

---

## 🔧 Pré-requisitos

- Python 3.10+ instalado e no jeito  
- Node.js + npm instalados  
- Conta e chave API OpenAI ou Gemini (se for usar modelos remotos)  

---

## ⚙️ Passo a passo para instalar e rodar

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/cupom-inteligente.git
cd cupom-inteligente
```
## 2. Backend — instalar dependências
cd backend
pip install -r requirements.txt

## 3. Configurar variáveis de ambiente (backend)
No diretório backend/, crie o arquivo .env com sua chave API:

# Usando OpenAI (padrão)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OU Google Gemini (opcional)
# GEMINI_API_KEY=ya29.xxxxxx
Dica: Gere a chave OpenAI em https://platform.openai.com/api-keys
Para Gemini, use o console do Google/AI Studio.

##4. Rodar o backend
Dentro da pasta backend/, execute:

uvicorn api_rest:app --host 0.0.0.0 --port 8000 --reload

Ou, se estiver na raiz do projeto:

uvicorn backend.api_rest:app --host 0.0.0.0 --port 8000 --reload

A API ficará acessível em:

http://SEU_IP_LOCAL:8000
(Substitua SEU_IP_LOCAL pelo IP do seu PC, ex.: 192.168.1.8)

##5. Frontend — instalar e iniciar

cd ../frontend
npm install
Opção A — Editar API_URL direto no código
Abra src/components/ChatApp.vue e altere:

const API_URL = 'http://192.168.1.8:8000' // seu IP local

Opção B — Usar variável de ambiente (Vite)
Crie .env na pasta frontend/ com:

VITE_API_URL=http://192.168.1.8:8000

No código, use:

const API_URL = import.meta.env.VITE_API_URL

## 6. Rodar o frontend (acesso via Wi-Fi)

npm run dev -- --host 0.0.0.0
# ou, se usa "serve":
# npm run serve -- --host 0.0.0.0

Acesse pelo navegador no PC ou celular (mesma rede Wi-Fi):

http://SEU_IP_LOCAL:5173
(Pode variar a porta: 8080, 3000...)

## 7. Testando no celular (mesma rede Wi-Fi)
Backend rodando com --host 0.0.0.0

Frontend com API_URL apontando para http://SEU_IP_LOCAL:8000

Abra no navegador do celular: http://SEU_IP_LOCAL:5173

Libere portas 8000 e 5173 no firewall do Windows, se precisar

## 🧪 Testes / Exemplos de perguntas
"O que é um cupom fiscal?"

"Quais impostos aparecem em um cupom fiscal da Paraíba?"

"O que significa ICMS?"

"Quais informações importantes eu devo checar no cupom fiscal?"

"Como guardar meus cupons para possíveis reembolsos ou garantias?"

## 🔍 Troubleshooting rápido
OPENAI_API_KEY não encontrada? Confira o .env na pasta backend/ e se load_dotenv() está lendo certinho

Erro Cannot import module 'backend'? Verifique se tem __init__.py em backend/ ou rode o uvicorn no lugar certo

CORS? Já liberado para dev (allow_origins=["*"]), mas ajuste para produção

Mudou de OpenAI para Gemini? Ajuste agentes, imports e libs (openai vs langchain-google-genai)

## 🧾 Estrutura do projeto (resumida)
bash
Copiar
Editar
cupom-inteligente/
├── backend/
│   ├── api_rest.py         # FastAPI app
│   ├── main.py             # Inicialização + CrewAI
│   ├── agents/             # Gerente, desenvolvedor, analista
│   ├── conhecimento/       # PDFs, docs e dados
│   └── .env                # Chave API OpenAI ou Gemini
├── frontend/
│   ├── src/
│   │   ├── components/     # ChatApp.vue e outros
│   │   └── ...
│   └── package.json
└── README.md
