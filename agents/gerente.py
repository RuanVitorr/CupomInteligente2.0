import os
from dotenv import load_dotenv
from crewai import Agent
from langchain.chat_models import ChatOpenAI  # Importa o OpenAI certinho

load_dotenv()

def criar_gerente(conhecimento, openai_key):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",       # ou "gpt-4" se quiser gastar mais crédito (e dinheiro)
        temperature=0.7,
        max_tokens=300,
        openai_api_key=os.getenv("OPENAI_API_KEY")  # pega chave do .env
    )

    return Agent(
        role="Gerente de Projetos",
        goal="Interpretar o objetivo do usuário e distribuir tarefas sobre cupons fiscais da Paraíba",
        backstory=(
            "Você é um especialista em cupons fiscais, especialmente no modelo utilizado na Paraíba. "
            "Use os seguintes documentos para ajudar:\n"
            f"{conhecimento}"
        ),
        memory=True,
        verbose=True,
        allow_delegation=True,
        llm=llm
    )
