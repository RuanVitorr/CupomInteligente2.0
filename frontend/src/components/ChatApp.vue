<template>
  <div class="chat-container">
    <div class="chat-messages">
      <div
        v-for="(msg, index) in mensagens"
        :key="index"
        :class="[
          'message px-4 py-2 rounded-chat max-w-[75%] mb-2',
          msg.deUsuario ? 'bg-blue-600 text-white self-end' : 'bg-gray-200 text-gray-900 self-start'
        ]"
        :style="{ alignSelf: msg.deUsuario ? 'flex-end' : 'flex-start' }"
      >
        {{ msg.texto }}
      </div>
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
import { ref } from 'vue'

interface Mensagem {
  texto: string
  deUsuario: boolean
}

export default {
  name: 'ChatApp',
  setup() {
    const mensagens = ref<Mensagem[]>([])
    const novaMensagem = ref('')

    async function enviarMensagem() {
      if (!novaMensagem.value.trim()) return

      mensagens.value.push({ texto: novaMensagem.value, deUsuario: true })

      try {
        const response = await fetch('http://localhost:8000/perguntar', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pergunta: novaMensagem.value }),
        })
        const data = await response.json()
        mensagens.value.push({ texto: data.resposta, deUsuario: false })
      } catch (error) {
        mensagens.value.push({ texto: 'Erro ao conectar com a API.', deUsuario: false })
      }

      novaMensagem.value = ''
    }

    return { mensagens, novaMensagem, enviarMensagem }
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 1rem auto;
  height: 90vh;
  display: flex;
  flex-direction: column;
  background: #121212; /* fundo preto escuro */
  box-shadow: 0 4px 10px rgb(0 0 0 / 0.5);
  border-radius: 1rem;
  padding: 1rem;
  color: #e0e0e0; /* texto claro */
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding-right: 1rem;
  margin-bottom: 1rem;
  scrollbar-width: thin;
  scrollbar-color: #3b82f6 #1f1f1f;
}

/* Scrollbar para dark mode */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background-color: #3b82f6; /* azul */
  border-radius: 4px;
}
::-webkit-scrollbar-track {
  background-color: #1f1f1f;
}

.message {
  word-wrap: break-word;
  white-space: pre-line;
}

.rounded-chat {
  border-radius: 1rem;
}

.chat-input-form {
  display: flex;
  gap: 0.5rem;
}

.chat-input {
  flex-grow: 1;
  padding: 0.5rem 1rem;
  border: 1px solid #333;
  border-radius: 9999px;
  outline: none;
  background-color: #222;
  color: #eee;
  transition: border-color 0.3s;
}
.chat-input::placeholder {
  color: #999;
}
.chat-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 5px #3b82f6;
}

.chat-button {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0 1.25rem;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}
.chat-button:hover {
  background-color: #2563eb;
}

/* Cores das mensagens adaptadas pro dark */
.message.bg-blue-600 {
  background-color: #2563eb !important; /* azul mais escuro */
  color: #fff;
}
.message.bg-gray-200 {
  background-color: #333 !important; /* cinza escuro */
  color: #eee;
}
</style>


