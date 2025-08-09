from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from main import rodar_crew_com_mensagem

# Cria a instância da API
app = FastAPI(title="AFRAFEP API", version="1.0")

# Configura CORS para permitir o front acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois pode trocar para o domínio do seu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados da requisição
class PerguntaRequest(BaseModel):
    pergunta: str

# Endpoint para fazer pergunta
@app.post("/perguntar")
async def perguntar(request: PerguntaRequest):
    try:
        resposta = rodar_crew_com_mensagem(request.pergunta)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de teste
@app.get("/")
async def root():
    return {"mensagem": "API AFRAFEP está no ar 🚀"}

# Executa o servidor se rodar direto
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
