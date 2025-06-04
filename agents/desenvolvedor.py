from crewai import Agent
from langchain_openai import ChatOpenAI
import os


def criar_desenvolvedor(conhecimento):
    # Cria a instância correta do modelo LLM
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0.7,
        max_tokens=600,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE")  # pega da variável .env
    )
    # conhecimento é parâmetro, é passado pra cá
    return Agent(
    role="Desenvolvedor Técnico",
    goal="Gerar código, ajustar prompts e configurações para soluções envolvendo cupons fiscais da Paraíba",
    backstory=f"Você conhece a fundo os detalhes técnicos dos cupons fiscais da Paraíba e usa documentos internos para desenvolver as melhores soluções.\n\nConhecimento:\n{conhecimento}",
    memory=True,
    verbose=True,
    allow_delegation=True,
    llm=llm
    )
