from crewai import Agent
from langchain_openai import ChatOpenAI
import os

def criar_gerente(conhecimento):
    # Cria a instância correta do modelo LLM
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0.7,
        max_tokens=600,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE")  # pega da variável .env
    )

    return Agent(
        role="Gerente de Projetos",
        goal="Interpretar o objetivo do usuário e distribuir tarefas sobre cupons fiscais da Paraíba",
        backstory=f"Você é um especialista em cupons fiscais, especialmente no modelo utilizado na Paraíba. Use os seguintes documentos para ajudar:\n{conhecimento}",
        memory=True,
        verbose=True,
        allow_delegation=True,
        llm=llm  # Agora sim, um LLM de verdade
    )
