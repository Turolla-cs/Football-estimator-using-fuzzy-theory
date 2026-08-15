from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot.chat import process_chat_message, system_instruction

app = FastAPI()

origens_permitidas = [
    "http://localhost:5500", 
    "http://127.0.0.1:5500",  
    "http://localhost:3000"    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

messages = [{"role": "system", "content": system_instruction}]

class MensagemUsuario(BaseModel):
    mensagem: str

@app.post("/api/chat")
async def chat_com_ia(dados: MensagemUsuario):
    try:
        resposta = process_chat_message(messages, dados.mensagem)
        return {"resposta": resposta}
    except Exception as e:
        print(f"[Error]: {e}")
        return {"resposta": "Houve um problema na base tática. Tente novamente mais tarde."}