<template>
  <div class="chat-room">
    <div class="chat-header">
      <h2>{{ roomName }}</h2>
      <div class="header-buttons">
        <button @click="showInviteModal = true" class="invite-btn">초대</button>
        <button @click="leaveRoom" class="leave-btn">나가기</button>
      </div>
    </div>
    
    <div class="messages-container">
      <div v-for="message in messages" 
           :key="message.id" 
           :class="['message', message.sender_id === currentUserId ? 'my-message' : '']">
        <div class="message-content">
          {{ message.content }}
        </div>
        <div class="message-info">
          <span class="username">{{ message.username }}</span>
          <span class="time">{{ formatTime(message.created_at) }}</span>
        </div>
      </div>
    </div>

    <div class="message-input">
      <input 
        v-model="newMessage" 
        @keyup.enter="sendMessage"
        placeholder="메시지를 입력하세요" />
      <button @click="sendMessage">전송</button>
    </div>

    <div v-if="showInviteModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>사용자 초대</h3>
          <button class="close-btn" @click="showInviteModal = false">&times;</button>
        </div>
        <input 
          v-model="searchTerm"
          class="search-input"
          placeholder="이메일로 검색..."
          @input="searchUsers"
        >
        <div class="user-list">
          <div v-for="user in searchResults" :key="user.id" class="user-item">
            <span>{{ user.email }}</span>
            <button @click="inviteUser(user.id)" class="invite-user-btn">초대</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatRoom',
  props: {
    roomId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      roomName: '',
      messages: [],
      newMessage: '',
      currentUserId: null,
      ws: null,
      showInviteModal: false,
      searchTerm: '',
      searchResults: [],
    }
  },
  async created() {
    await this.initializeRoom();
    this.connectWebSocket();
  },
  beforeDestroy() {
    if (this.ws) {
      this.ws.close();
    }
  },
  methods: {
    async initializeRoom() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/chat/rooms/${this.roomId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          credentials: 'include'
        });
        const data = await response.json();
        this.roomName = data.name;
        this.messages = data.messages;
        this.currentUserId = data.currentUserId;
        
        console.log('Current User ID:', this.currentUserId);
        console.log('First message sender_id:', this.messages[0]?.sender_id);
      } catch (err) {
        console.error('채팅방 정보를 불러오는데 실패했습니다:', err);
      }
    },
    connectWebSocket() {
      const token = localStorage.getItem('token');
      this.ws = new WebSocket(`ws://localhost:8000/ws/chat/${this.roomId}?token=${token}`);
      
      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log('받은 메시지:', message);
        if (!Array.isArray(this.messages)) {
          this.messages = [];
        }
        this.messages.push(message);
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      };
    },
    async sendMessage() {
      if (!this.newMessage.trim()) return;
      
      try {
        const message = {
          content: this.newMessage,
          room_id: this.roomId,
          sender_id: this.currentUserId
        };
        
        this.ws.send(JSON.stringify(message));
        this.newMessage = '';
      } catch (error) {
        console.error('메시지 전송 실패:', error);
      }
    },
    formatTime(timestamp) {
      if (!timestamp) {
        console.log('timestamp is missing:', timestamp);
        return '';
      }
      
      try {
        const date = new Date(timestamp);
        const dateStr = date.toLocaleDateString('ko-KR', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
        const timeStr = date.toLocaleTimeString('ko-KR', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        });
        return `${dateStr} ${timeStr}`;
      } catch (error) {
        console.error('시간 형식 변환 오류:', error, timestamp);
        return '';
      }
    },
    scrollToBottom() {
      const container = this.$refs.messageContainer;
      container.scrollTop = container.scrollHeight;
    },
    async leaveRoom() {
      try {
        const token = localStorage.getItem('token');
        await fetch(`http://localhost:8000/chat/rooms/${this.roomId}/leave`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          credentials: 'include'
        });
        this.$router.push('/chat');
      } catch (err) {
        console.error('채팅방 나가기에 실패했습니다:', err);
      }
    },
    async searchUsers() {
      if (!this.searchTerm) {
        this.searchResults = [];
        return;
      }
      
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/users/search?q=${this.searchTerm}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.searchResults = await response.json();
      } catch (err) {
        console.error('사용자 검색 실패:', err);
      }
    },
    async inviteUser(userId) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/chat/${this.roomId}/invite/${userId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          alert('사용자가 초대되었습니다.');
          this.showInviteModal = false;
        } else {
          throw new Error('초대 실패');
        }
      } catch (err) {
        alert('사용자 초대에 실패했습니다.');
        console.error('초대 실패:', err);
      }
    }
  }
}
</script>

<style scoped>
.chat-room {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 20px;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.leave-btn {
  padding: 8px 15px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.leave-btn:hover {
  background-color: #cc0000;
}

.messages-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow-y: auto;
}

.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
  max-width: 70%;
  align-self: flex-start;
}

.message-content {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 10px;
  word-wrap: break-word;
}

.message-info {
  font-size: 0.8em;
  color: #666;
  margin-top: 5px;
}

.my-message {
  align-self: flex-end;
}

.my-message .message-content {
  background-color: #007bff;
  color: white;
}

.my-message .message-info {
  text-align: right;
}

.username {
  font-weight: bold;
  margin-right: 10px;
}

.time {
  color: #666;
}

.message-input {
  display: flex;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px solid #ddd;
}

.message-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.message-input button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.invite-btn {
  padding: 8px 15px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.invite-btn:hover {
  background-color: #1976D2;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 400px;
  max-width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-btn {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.user-list {
  display: flex;
  flex-direction: column;
  max-height: 300px;
  overflow-y: auto;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.invite-user-btn {
  padding: 6px 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.invite-user-btn:hover {
  background-color: #1976D2;
}
</style> 