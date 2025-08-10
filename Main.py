# main.py
import os
import traceback
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from crewai import Crew, Task
from langchain.chat_models import ChatOpenAI  # pra garantir que usa OpenAI

# Carrega variáveis de ambiente
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
print(f"Chave da API carregada: {'SIM' if openai_key else 'NÃO'}")

if not openai_key:
    raise ValueError("⚠️ OPENAI_API_KEY não encontrada no .env")

# Importa os agentes
from agents.gerente import criar_gerente
from agents.desenvolvedor import criar_desenvolvedor
from agents.analista import criar_analista


# ---------- ETAPA 1: Carrega conhecimento dos PDFs ----------
def carregar_conhecimento(pasta="conhecimento") -> str:
    documentos = []
    for arquivo in os.listdir(pasta):
        if not arquivo.lower().endswith(".pdf"):
            continue
        caminho_pdf = os.path.join(pasta, arquivo)
        loader = PyPDFLoader(caminho_pdf)
        documentos.extend(loader.load())
    return "\n".join([doc.page_content for doc in documentos])


# ---------- ETAPA 2: Inicializa agentes com LLM OpenAI ----------
conhecimento = carregar_conhecimento()

# Atualize os agentes para usarem ChatOpenAI com sua OPENAI_API_KEY
gerente = criar_gerente(conhecimento, openai_key)
desenvolvedor = criar_desenvolvedor(conhecimento, openai_key)
analista = criar_analista(conhecimento, openai_key)


# ---------- ETAPA 3: Função que executa a Crew ----------
def rodar_crew_com_mensagem(pergunta_usuario: str) -> str:
    task = Task(
        description=f"O usuário perguntou: \"{pergunta_usuario}\". Responda de forma clara, útil e em português brasileiro.",
        agent=analista,
        expected_output="Resposta bem estruturada, objetiva e em linguagem acessível ao cidadão brasileiro."
    )

    crew = Crew(
        agents=[analista],
        tasks=[task],
        verbose=False
    )

    try:
        resultado = crew.kickoff()

        if isinstance(resultado, str):
            return resultado.strip()

        for attr in ["final_output", "raw", "result", "output"]:
            if hasattr(resultado, attr):
                valor = getattr(resultado, attr)
                if isinstance(valor, str) and valor.strip():
                    return valor.strip()

        if hasattr(resultado, "outputs") and resultado.outputs:
            saidas = resultado.outputs
            if isinstance(saidas, list):
                for s in reversed(saidas):
                    for chave in ["output", "raw_output"]:
                        if isinstance(s, dict) and chave in s and isinstance(s[chave], str) and s[chave].strip():
                            return s[chave].strip()
                        elif hasattr(s, chave):
                            valor = getattr(s, chave)
                            if isinstance(valor, str) and valor.strip():
                                return valor.strip()

        return "⚠️ A IA não retornou resposta."

    except Exception as e:
        print("⚠️ Erro ao rodar a crew:")
        traceback.print_exc()

        erro = str(e).lower()
        if any(p in erro for p in ["rate_limit", "quota", "limit"]):
            return "⚠️ Limite de uso da API foi atingido. Tente novamente mais tarde."

        return f"⚠️ Erro inesperado: {type(e).__name__}: {str(e)}"