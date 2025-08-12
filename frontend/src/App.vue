<template>
  <div class="page-container">
    <!-- Cabeçalho -->
    <div class="floating-header">
      <div class="header-title">Cupom inteligente</div>
      <div class="header-user-icon" title="Usuário">&#128100;</div>
    </div>

    <!-- Área principal -->
    <main class="page-main">
      <ChatApp />
    </main>

    <!-- Aviso -->
    <div class="chat-warning">
      <p>O Cupom inteligente pode cometer erros. Considere verificar informações importantes.</p>
      <small>Versão 1.0</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import ChatApp from './components/ChatApp.vue'
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  background-color: #1f2937;
  color: #e0e0e0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.page-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Cabeçalho */
.floating-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.2rem;
}

.header-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: #4f46e5;
}

.header-user-icon {
  font-size: 1.5rem;
  color: #4f46e5;
}

/* Área principal com o chat */
.page-main {
  flex: 1;
  display: flex;
  justify-content: center;
  min-height: 0; /* ESSENCIAL p/ não forçar overflow */
}

.page-main > * {
  flex: 1;
  max-width: 900px;
  width: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0; /* evita que o conteúdo cresça demais */
}

/* Aviso */
.chat-warning {
  flex-shrink: 0;
  text-align: center;
  font-size: 0.7rem;
  color: #999;
  padding: 0.3rem;
  line-height: 1.2;
}

.chat-warning p {
  margin: 0;
}

.chat-warning small {
  font-weight: 600;
  display: block;
  margin-top: 0.1rem;
}
</style>
