<template>
  <div class="login-form">
    <h2>로그인</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>이메일:</label>
        <input 
          type="email" 
          v-model="email" 
          required 
          placeholder="이메일을 입력하세요" />
      </div>
      <div class="form-group">
        <label>비밀번호:</label>
        <input 
          type="password" 
          v-model="password" 
          required 
          placeholder="비밀번호를 입력하세요" />
      </div>
      <div class="button-group">
        <button type="submit">로그인</button>
        <button type="button" @click="goToSignUp" class="signup-btn">회원가입</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await fetch('http://localhost:8000/auth/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
          },
          credentials: 'include',
          body: `username=${encodeURIComponent(this.email)}&password=${encodeURIComponent(this.password)}`
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || '로그인 실패');
        }

        const data = await response.json();
        console.log('로그인 성공:', data); // 디버깅용
        localStorage.setItem('token', data.access_token);
        this.$router.push('/chat');
      } catch (err) {
        console.error('로그인 에러:', err);
        this.error = '로그인에 실패했습니다. 다시 시도해주세요.';
      }
    },
    goToSignUp() {
      this.$router.push('/signup');
    }
  }
}
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.signup-btn {
  background-color: #2196F3;
}

button {
  flex: 1;
  padding: 10px;
  color: white;
  border: none;
  cursor: pointer;
  background-color: #4CAF50;
}

.error {
  color: red;
  margin-top: 10px;
}
</style> 