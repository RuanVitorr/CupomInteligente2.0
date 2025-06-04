import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from crewai import Crew, Task
from langchain_openai import ChatOpenAI

load_dotenv()  # Carrega as variáveis do .env

# Acessar a API key assim:
openai_key = os.getenv("OPENAI_API_KEY")
#print("Minha chave é:", openai_key)  # Só pra testar

# Importa os agentes (você precisa já ter esses arquivos prontos em agents/)
from agents.gerente import criar_gerente
from agents.desenvolvedor import criar_desenvolvedor
from agents.analista import criar_analista

# Carrega variáveis de ambiente (ex: OPENAI_API_KEY)
load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

#/ ----------- Etapa 1: Carregar todos os PDFs da pasta "conhecimento" -----------
pasta_conhecimento = "conhecimento"

documentos = []

for arquivo in os.listdir(pasta_conhecimento):
    caminho_pdf = os.path.join(pasta_conhecimento, arquivo)
    loader = PyPDFLoader(caminho_pdf)
    documentos.extend(loader.load())

# Junta todo o conteúdo dos PDFs em um texto só (pra passar pros agentes)
conhecimento = "\n".join([doc.page_content for doc in documentos])

# Criar os agentes com o conhecimento
gerente = criar_gerente(conhecimento)
desenvolvedor = criar_desenvolvedor(conhecimento)
analista = criar_analista(conhecimento)

# ----------- Etapa 3: Criar as tarefas dos agentes com CrewAI -----------

entrada_usuario = "Preciso de um resumo explicando os impostos detalhados de um cupom fiscal da Paraíba."

task_gerente = Task(
    description=entrada_usuario,
    agent=gerente,
    expected_output="Resumo explicativo sobre os impostos detalhados de um cupom fiscal da Paraíba."
)

task_desenvolvedor = Task(
    description="Com base na instrução do gerente, gerar código ou explicação útil com base nos documentos sobre cupons fiscais.",
    agent=desenvolvedor,
    expected_output="Código ou explicação clara sobre os impostos do cupom fiscal da Paraíba."
)

task_analista = Task(
    description="Avaliar a resposta gerada, sugerir melhorias e relatar pontos importantes.",
    agent=analista,
    expected_output="Análise com sugestões de melhoria e pontos relevantes da explicação."
)


# ----------- Etapa 4: Rodar a Crew (os agentes trabalhando juntos) -----------
import traceback
crew = Crew(
    agents=[gerente, desenvolvedor, analista],
    tasks=[task_gerente, task_desenvolvedor, task_analista],
    verbose=True
)

try:
    resultado = crew.kickoff()
except Exception as e:
    print("Oxe, deu ruim na Crew! Erro capturado:")
    print(e)
    # Aqui você pode colocar um tratamento extra, tipo salvar log, mandar alerta, etc.
    traceback.print_exc()
    resultado = None  # ou algum valor padrão pra seguir o fluxo sem travar

# ----------- Etapa 5: Mostrar o resultado final -----------

print("\n=== RESULTADO FINAL ===\n")
print(resultado)
