<template>
  <div class="signup-form">
    <h2>회원가입</h2>
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
      <div class="form-group">
        <label>비밀번호 확인:</label>
        <input 
          type="password" 
          v-model="confirmPassword" 
          required 
          placeholder="비밀번호를 다시 입력하세요" />
      </div>
      <button type="submit">가입하기</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p class="login-link">
      이미 계정이 있으신가요? <router-link to="/">로그인하기</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'SignUpForm',
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      error: null
    }
  },
  methods: {
    async handleSubmit() {
      if (this.password !== this.confirmPassword) {
        this.error = '비밀번호가 일치하지 않습니다.';
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          referrerPolicy: 'no-referrer',
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            username: this.email.split('@')[0] // 임시 username 생성
          })
        });

        const data = await response.json();

        if (!response.ok) {
          // 서버에서 전달받은 구체적인 에러 메시지 표시
          this.error = data.detail || '회원가입에 실패했습니다.';
          return;
        }

        // 회원가입 성공 후 로그인 페이지로 이동
        this.$router.push('/');
      } catch (err) {
        console.error('회원가입 오류:', err);
        this.error = '서버 연결에 실패했습니다. 잠시 후 다시 시도해주세요.';
      }
    }
  }
}
</script>

<style scoped>
.signup-form {
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

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 10px;
}

.login-link {
  margin-top: 15px;
  text-align: center;
}

.login-link a {
  color: #4CAF50;
  text-decoration: none;
}
</style> 