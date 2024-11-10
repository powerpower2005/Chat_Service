<template>
  <div class="chat-layout">
    <header class="chat-header">
      <h1>채팅</h1>
      <button @click="logout" class="logout-btn">로그아웃</button>
    </header>
    <main class="chat-main">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'ChatLayout',
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.chat-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-header {
  background-color: #2196F3;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-main {
  flex: 1;
  padding: 2rem;
  background-color: #f5f5f5;
}

.logout-btn {
  background-color: transparent;
  border: 1px solid white;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style> 