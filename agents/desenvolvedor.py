from crewai import Agent
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def criar_desenvolvedor(conhecimento, openai_key):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=300,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    return Agent(
        role="Desenvolvedor Técnico",
        goal="Gerar código, ajustar prompts e configurações para soluções envolvendo cupons fiscais da Paraíba",
        backstory=(
            "Você conhece a fundo os detalhes técnicos dos cupons fiscais da Paraíba e "
            "usa documentos internos para desenvolver as melhores soluções.\n\n"
            f"Conhecimento:\n{conhecimento}"
        ),
        memory=True,
        verbose=True,
        allow_delegation=True,
        llm=llm
    )
