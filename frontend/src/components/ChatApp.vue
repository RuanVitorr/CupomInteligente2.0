<template>
  <div class="chat-container">
    <div ref="chatMessages" class="chat-messages">
      <transition-group name="fade-slide" tag="div">
        <div
          v-for="(msg, index) in mensagens"
          :key="index"
          :class="[
            'message px-5 py-3 rounded-chat max-w-[75%] mb-3',
            msg.deUsuario ? 'user-msg' : 'bot-msg'
          ]"
          :style="{ alignSelf: msg.deUsuario ? 'flex-end' : 'flex-start' }"
        >
          {{ msg.texto }}
        </div>
      </transition-group>
    </div>

    <form @submit.prevent="enviarMensagem" class="chat-input-form">
      <input
        v-model="novaMensagem"
        type="text"
        placeholder="Digite sua mensagem..."
        class="chat-input"
        autocomplete="off"
      />
      <button type="submit" class="chat-button">Enviar</button>
    </form>
  </div>
</template>

<script lang="ts">
import { ref, nextTick } from 'vue'

interface Mensagem {
  texto: string
  deUsuario: boolean
}

export default {
  name: 'ChatApp',
  setup() {
    const API_URL = 'http://192.168.1.x:8000'  // troca aqui pro IP do seu PC
    const mensagens = ref<Mensagem[]>([])
    const novaMensagem = ref('')
    const chatMessages = ref<HTMLElement | null>(null)

    async function enviarMensagem() {
      if (!novaMensagem.value.trim()) return

      mensagens.value.push({ texto: novaMensagem.value, deUsuario: true })

      novaMensagem.value = ''  // limpa rápido

      await nextTick()
      scrollToBottom()

      try {
        const response = await fetch('http://localhost:8000/perguntar', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pergunta: mensagens.value[mensagens.value.length - 1].texto }),
        })
        const data = await response.json()
        mensagens.value.push({ texto: data.resposta, deUsuario: false })

        await nextTick()
        scrollToBottom()
      } catch (error) {
        mensagens.value.push({ texto: 'Erro ao conectar com a API.', deUsuario: false })

        await nextTick()
        scrollToBottom()
      }
    }

    function scrollToBottom() {
      if (chatMessages.value) {
        chatMessages.value.scrollTo({
          top: chatMessages.value.scrollHeight,
          behavior: 'smooth',
        })
      }
    }

    return { mensagens, novaMensagem, enviarMensagem, chatMessages }
  },
}
</script>


<style scoped>
.chat-container {
  max-width: 600px;
  margin: 0 auto;
  flex: 1; /* ocupa o espaço disponível */
  display: flex;
  flex-direction: column;
  min-height: 0; /* ESSENCIAL para o flex funcionar direito */
  background: #181a1f; /* cinza escuro mais suave */
  box-shadow: 0 10px 30px rgb(0 0 0 / 0.6);
  border-radius: 1.5rem;
  padding: 1.5rem 2rem;
  color: #ddd;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding-right: 1rem;
  margin-bottom: 1.5rem;
  scrollbar-width: thin;
  scrollbar-color: #4f46e5 #1f1f1f;
}

/* Scrollbar para dark mode */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background-color: #4f46e5; /* roxo moderno */
  border-radius: 6px;
}
::-webkit-scrollbar-track {
  background-color: #1f1f1f;
}

.message {
  margin: 8px 0; /* mais espaço vertical */
  padding: 14px 20px; /* bolha mais confortável */
  max-width: 75%;
  word-wrap: break-word;
  white-space: pre-line;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgb(0 0 0 / 0.25);
  transition: background-color 0.3s ease;
}

/* Usuário */
.user-msg {
  align-self: flex-end;
  background-color: #4f46e5;
  color: #f0f0f0;
  box-shadow: 0 6px 12px rgb(79 70 229 / 0.5);
  border-top-right-radius: 4px; /* pontinha reta do lado direito */
  border-bottom-right-radius: 20px;
  border-bottom-left-radius: 20px;
}

/* Bot */
.bot-msg {
  align-self: flex-start;
  background-color: #272b33;
  color: #ccc;
  box-shadow: 0 6px 12px rgb(39 43 51 / 0.5);
  border-top-left-radius: 4px; /* pontinha reta do lado esquerdo */
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
}

.chat-input-form {
  display: flex;
  gap: 1rem;
}

.chat-input {
  flex-grow: 1;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 9999px;
  outline: none;
  background-color: #272b33;
  color: #eee;
  font-size: 1rem;
  box-shadow: inset 0 0 6px rgb(0 0 0 / 0.5);
  transition: box-shadow 0.3s, background-color 0.3s;
}

.chat-input::placeholder {
  color: #666;
  font-style: italic;
}

.chat-input:focus {
  background-color: #323946;
  box-shadow: 0 0 12px #4f46e5;
}

.chat-button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 0 1.75rem;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 6px 14px rgb(79 70 229 / 0.7);
  transition: background-color 0.3s, box-shadow 0.3s;
}

.chat-button:hover {
  background-color: #3c36b0;
  box-shadow: 0 8px 20px rgb(60 54 176 / 0.85);
}

/* Animação das mensagens */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.15s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(5px);
}

.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(5px);
}

</style>
