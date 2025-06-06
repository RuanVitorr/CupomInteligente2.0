import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from crewai import Crew, Task
from langchain_openai import ChatOpenAI

load_dotenv()  # Carrega as variáveis do .env

# Acessar a API key assim:
openai_key = os.getenv("OPENAI_API_KEY")
#print("Minha chave é:", openai_key)  # test

# Importa os agentes
from agents.gerente import criar_gerente
from agents.desenvolvedor import criar_desenvolvedor
from agents.analista import criar_analista

# Carrega variáveis de ambiente (OPENAI_API_KEY)
load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

#/ ----------- Etapa 1: Carregar todos os PDFs da pasta "conhecimento" -----------
pasta_conhecimento = "conhecimento"

documentos = []

for arquivo in os.listdir(pasta_conhecimento):
    caminho_pdf = os.path.join(pasta_conhecimento, arquivo)
    loader = PyPDFLoader(caminho_pdf)
    documentos.extend(loader.load())

# Junta todo o conteúdo dos PDFs em um texto só
conhecimento = "\n".join([doc.page_content for doc in documentos])

# Criar os agentes com o conhecimento
gerente = criar_gerente(conhecimento)
desenvolvedor = criar_desenvolvedor(conhecimento)
analista = criar_analista(conhecimento)

# ----------- Etapa 2: Criar as tarefas dos agentes com CrewAI -----------

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


# ----------- Etapa 3: Rodar a Crew, agentes trabalhando juntos -----------
import traceback

crew = Crew(
    agents=[gerente, desenvolvedor, analista],
    tasks=[task_gerente, task_desenvolvedor, task_analista],
    verbose=True
)

try:
    resultado = crew.kickoff()
except Exception as e:
    print("deu ruim na Crew! Erro capturado:")
    print(e)
    traceback.print_exc()
    resultado = None

# ----------- Etapa 4: Mostrar o resultado final -----------

print("\n=== DEBUG: resultado da crew ===\n")
print(resultado)
print(type(resultado))

# Tenta pegar a resposta segura
resposta_final = getattr(resultado, "final_output", None) or getattr(resultado, "output", None) or ""

print("\n=== RESULTADO FINAL ===\n")
print(resposta_final)

print("\n=== DEBUG COMPLETO DO OBJETO ===\n")
print(dir(resultado))  # Mostra todos os atributos disponíveis
if resultado:
    try:
        print(resultado.dict())  # Mostra o conteúdo completo em dicionário, se suportado
    except Exception:
        print("Não foi possível converter resultado para dict.")

# Verificar se a resposta parece incompleta
if isinstance(resposta_final, str) and resposta_final.endswith(" ..."):
    resposta_usuario = input("\n⚠️ A resposta parece estar incompleta. Quer que eu tente pedir a continuação? (sim/não): ").strip().lower()

    if resposta_usuario in ["sim", "s", "claro", "por favor", "sim!"]:
        print("\n👉 Pedindo continuação da resposta...\n")

        # Cria nova tarefa só com o analista pra continuar a resposta
        task_continuacao = Task(
            description="Continue a análise a partir da resposta anterior, finalizando o que ficou incompleto.",
            agent=analista,
            expected_output="Continuação da análise anterior, completando a resposta."
        )

        crew_continuacao = Crew(
            agents=[analista],
            tasks=[task_continuacao],
            verbose=True
        )

        try:
            resultado_continuacao = crew_continuacao.kickoff()
            resposta_continuacao = getattr(resultado_continuacao, "final_output", None) or getattr(resultado_continuacao, "output", None) or ""
            print("\n=== CONTINUAÇÃO DA RESPOSTA ===\n")
            print(resposta_continuacao)
        except Exception as e:
            print("⚠️ Deu pau na continuação!")
            print(e)


# ----------- Etapa 5: Rodar a Crew (os agentes trabalhando juntos) -----------
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
    traceback.print_exc()
    resultado = None

# ----------- Etapa 6: Mostrar o resultado final -----------

print("\n=== DEBUG: resultado da crew ===\n")
print(resultado)
print(type(resultado))

# Tenta pegar a resposta segura
resposta_final = getattr(resultado, "final_output", None) or getattr(resultado, "output", None) or ""

print("\n=== RESULTADO FINAL ===\n")
print(resposta_final)

print("\n=== DEBUG COMPLETO DO OBJETO ===\n")
print(dir(resultado))  # Mostra todos os atributos disponíveis
if resultado:
    try:
        print(resultado.dict())  # Mostra o conteúdo completo em dicionário, se suportado
    except Exception:
        print("Não foi possível converter resultado para dict.")

# Verificar se a resposta parece incompleta
if isinstance(resposta_final, str) and resposta_final.endswith(" ..."):
    resposta_usuario = input("\n⚠️ A resposta parece estar incompleta. Quer que eu tente pedir a continuação? (sim/não): ").strip().lower()

    if resposta_usuario in ["sim", "s", "claro", "por favor", "sim!"]:
        print("\n👉 Pedindo continuação da resposta...\n")

        # Cria nova tarefa só com o analista pra continuar a resposta
        task_continuacao = Task(
            description="Continue a análise a partir da resposta anterior, finalizando o que ficou incompleto.",
            agent=analista,
            expected_output="Continuação da análise anterior, completando a resposta."
        )

        crew_continuacao = Crew(
            agents=[analista],
            tasks=[task_continuacao],
            verbose=True
        )

        try:
            resultado_continuacao = crew_continuacao.kickoff()
            resposta_continuacao = getattr(resultado_continuacao, "final_output", None) or getattr(resultado_continuacao, "output", None) or ""
            print("\n=== CONTINUAÇÃO DA RESPOSTA ===\n")
            print(resposta_continuacao)
        except Exception as e:
            print("⚠️ Deu pau na continuação!")
            print(e)


import traceback


def rodar_crew_com_mensagem(pergunta_usuario: str) -> str:
    
    task_resposta_direta = Task(
        description=f"O usuário perguntou: \"{pergunta_usuario}\". Sua principal responsabilidade é analisar esta pergunta e fornecer uma resposta completa, objetiva, educativa e em português brasileiro.",
        agent=analista, 
                        
        expected_output="Uma resposta textual, clara, bem formatada e em português brasileiro, que responda diretamente à pergunta do usuário."
    )

    
    crew_pergunta = Crew(
        agents=[analista], 
        tasks=[task_resposta_direta], 
        verbose=False 
    )

    try:
        resultado = crew_pergunta.kickoff()

        # Logs de Debug no backend (console onde o Streamlit/Python está rodando)
        print("\n=== DEBUG Backend: rodar_crew_com_mensagem ===")
        print(f"Pergunta do Usuário: {pergunta_usuario}")
        print(f"Tipo de 'resultado' recebido da crew.kickoff(): {type(resultado)}")
        print(f"Conteúdo de 'resultado': {resultado}")
        if not isinstance(resultado, str) and resultado is not None:
            print(f"Atributos de 'resultado' (se objeto): {dir(resultado)}")
        print("--- Fim do DEBUG Backend ---\n")

        # 1. Verifica se o resultado já é a string final (mais comum com verbose=False e tasks simples)
        if isinstance(resultado, str) and resultado.strip():
            return resultado.strip()

        # 2. Tenta 'final_output' (padrão em versões mais recentes da CrewAI para o resultado consolidado)
        if hasattr(resultado, "final_output") and isinstance(resultado.final_output, str) and resultado.final_output.strip():
            return resultado.final_output.strip()

        # 3. Tenta 'raw' (saída bruta do último task, comum)
        if hasattr(resultado, "raw") and isinstance(resultado.raw, str) and resultado.raw.strip():
            return resultado.raw.strip()

        # 4. Tenta 'result' (outra propriedade possível)
        if hasattr(resultado, "result") and isinstance(resultado.result, str) and resultado.result.strip():
            return resultado.result.strip()

        # 5. Tenta extrair de 'outputs' (se for uma lista de tasks outputs)
        if hasattr(resultado, "outputs") and resultado.outputs:
            if isinstance(resultado.outputs, list) and len(resultado.outputs) > 0:
                # Tenta pegar o output da última task na lista de outputs
                ultimo_output_obj = resultado.outputs[-1]
                if isinstance(ultimo_output_obj, str) and ultimo_output_obj.strip():
                    return ultimo_output_obj.strip()
                if hasattr(ultimo_output_obj, "output") and isinstance(ultimo_output_obj.output, str) and ultimo_output_obj.output.strip():
                    return ultimo_output_obj.output.strip()
                if hasattr(ultimo_output_obj, "raw_output") and isinstance(ultimo_output_obj.raw_output, str) and ultimo_output_obj.raw_output.strip():
                    return ultimo_output_obj.raw_output.strip()
                # Se o objeto de output for um dicionário
                if isinstance(ultimo_output_obj, dict):
                    if "output" in ultimo_output_obj and isinstance(ultimo_output_obj["output"], str) and ultimo_output_obj["output"].strip():
                        return ultimo_output_obj["output"].strip()
                    if "raw_output" in ultimo_output_obj and isinstance(ultimo_output_obj["raw_output"], str) and ultimo_output_obj["raw_output"].strip():
                        return ultimo_output_obj["raw_output"].strip()
            elif isinstance(resultado.outputs, str) and resultado.outputs.strip(): # Caso 'outputs' seja diretamente a string
                 return resultado.outputs.strip()

        # 6. Tenta extrair do último 'task_output' em 'tasks_outputs' (se disponível)
        if hasattr(resultado, "tasks_outputs") and isinstance(resultado.tasks_outputs, list) and resultado.tasks_outputs:
            ultimo_task_output = resultado.tasks_outputs[-1]
            if hasattr(ultimo_task_output, "result") and isinstance(ultimo_task_output.result, str) and ultimo_task_output.result.strip():
                return ultimo_task_output.result.strip()
            if hasattr(ultimo_task_output, "raw") and isinstance(ultimo_task_output.raw, str) and ultimo_task_output.raw.strip(): # 'raw' é comum aqui
                return ultimo_task_output.raw.strip()
            if isinstance(ultimo_task_output, str) and ultimo_task_output.strip(): # Se o próprio task_output for a string
                return ultimo_task_output.strip()

        # 7. Como último recurso, converte o objeto resultado para string, se não for None e não vazio.
        
        if resultado is not None:
            str_resultado = str(resultado).strip()
            # Evita retornar representações de objeto genéricas como "<crewai. κάποιο.Objeto object at 0x...>"
            # ou strings muito curtas que provavelmente não são a resposta.
            if str_resultado and len(str_resultado) > 20 and not str_resultado.startswith("<") and not str_resultado.endswith(">"):
                return str_resultado

        return "⚠️ A IA ficou em silêncio... Nenhuma resposta textual foi gerada ou extraída."

    except Exception as e:
        print(f"⚠️ EXCEÇÃO na função rodar_crew_com_mensagem:")
        traceback.print_exc() # Imprime o traceback completo no console do backend
        
        error_message = str(e).lower()
        if "rate_limit_error" in error_message or \
           "ratelimiterror" in error_message or \
           "quota" in error_message or \
           "limit" in error_message or \
           "insufficient_quota" in error_message:
            return "⚠️ Sistema sobrecarregado ou limite de uso da API atingido. Por favor, tente novamente mais tarde ou verifique sua cota."
        
        # Tenta fornecer uma mensagem de erro um pouco mais amigável se possível
        detailed_error = f"{type(e).__name__}: {str(e)}"
        return f"⚠️ Ops! Ocorreu um erro ao processar sua pergunta ({detailed_error}). Por favor, tente novamente."