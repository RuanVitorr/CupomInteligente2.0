from crewai import Agent
from langchain_openai import ChatOpenAI
import os


def criar_analista(conhecimento):
    # Cria a instância correta do modelo LLM
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0.7,
        max_tokens=600,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE")  # pega da variável .env
    )
    return Agent( 
    role="Analista de Resultados",
    goal="Avaliar a saída, gerar relatórios e propor melhorias baseadas nos cupons fiscais da Paraíba",
    backstory=f"Você é um especialista em análise de resultados e conhece profundamente os cupons fiscais da Paraíba, usando documentos internos para tomar decisões precisas.\n\nConhecimento:\n{conhecimento}",
    memory=True,
    verbose=True,
    allow_delegation=True,
    llm=llm
    )