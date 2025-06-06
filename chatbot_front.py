import streamlit as st
from Main import rodar_crew_com_mensagem  # função que roda a Crew com a pergunta do usuário

st.set_page_config(page_title="Cupom Inteligente", page_icon="🧾", layout="centered")

st.title("🤖 Cupom Inteligente")

# Inicializa o estado da conversa
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Mostra toda a conversa
for msg in st.session_state.mensagens:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Campo de entrada do usuário
pergunta = st.chat_input("Digite sua pergunta sobre o cupom fiscal ou ICMS...")

if pergunta:
    # Armazena a pergunta do cabra na conversa
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    st.chat_message("user").markdown(pergunta)

    # Responde com a inteligência da Crew
    with st.spinner("Consultando a inteligência fiscal..."):
        try:
            resposta = rodar_crew_com_mensagem(pergunta)
        except Exception as e:
            resposta = f"⚠️ Deu erro: {str(e)}"

    # Armazena e mostra a resposta do assistente
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    st.chat_message("assistant").markdown(resposta)

