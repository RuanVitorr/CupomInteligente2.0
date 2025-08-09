from crewai import Agent
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def criar_analista(conhecimento, openai_key):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=300,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    return Agent(
        role="Analista de Resultados",
        goal="Avaliar a saída, gerar relatórios e propor melhorias baseadas nos cupons fiscais da Paraíba",
        backstory=(
            "Você é um especialista em análise de resultados e conhece profundamente os cupons fiscais da Paraíba, "
            "usando documentos internos para tomar decisões precisas.\n\n"
            f"Conhecimento:\n{conhecimento}"
        ),
        memory=True,
        verbose=True,
        allow_delegation=True,
        llm=llm
    )
