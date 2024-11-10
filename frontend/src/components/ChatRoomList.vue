<template>
  <div class="chat-room-list">
    <h2>채팅방 목록</h2>
    <button @click="showCreateRoom = true" class="create-room-btn">
      새 채팅방 만들기
    </button>
    
    <div v-if="showCreateRoom" class="create-room-form">
      <input 
        v-model="newRoomName" 
        placeholder="채팅방 이름을 입력하세요" />
      <button @click="createRoom">생성</button>
      <button @click="showCreateRoom = false">취소</button>
    </div>

    <div class="room-list">
      <div 
        v-for="room in rooms" 
        :key="room.id" 
        class="room-item"
        @click="joinRoom(room.id)"
      >
        <h3>{{ room.name }}</h3>
        <p>참가자: {{ room.participants.length }}명</p>
      </div>
    </div>

    <input 
      type="text" 
      v-model="searchQuery" 
      placeholder="채팅방 검색" />
  </div>
</template>

<script>
export default {
  name: 'ChatRoomList',
  data() {
    return {
      rooms: [],
      showCreateRoom: false,
      newRoomName: '',
      searchQuery: ''
    }
  },
  async created() {
    await this.fetchRooms();
  },
  methods: {
    async fetchRooms() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/chat/rooms', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          credentials: 'include'
        });
        
        if (!response.ok) {
          throw new Error('채팅방 목록을 가져오는데 실패했습니다');
        }
        
        this.rooms = await response.json();
      } catch (err) {
        console.error('채팅방 목록을 불러오는데 실패했습니다:', err);
      }
    },
    async createRoom() {
      try {
        if (!this.newRoomName.trim()) {
          console.error('채팅방 이름을 입력해주세요');
          return;
        }

        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/chat/rooms', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            name: this.newRoomName
          })
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || '채팅방 생성에 실패했습니다');
        }
        
        const newRoom = await response.json();
        this.rooms.push(newRoom);
        this.showCreateRoom = false;
        this.newRoomName = '';
      } catch (err) {
        console.error('채팅방 생성 에러:', err);
        alert('채팅방 생성에 실패했습니다: ' + err.message);
      }
    },
    async joinRoom(roomId) {
      this.$router.push(`/chat/${roomId}`);
    }
  }
}
</script>

<style scoped>
.chat-room-list {
  padding: 20px;
}

.create-room-btn {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.room-item {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 10px;
  cursor: pointer;
}

.room-item:hover {
  background-color: #f5f5f5;
}

.create-room-form {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
}

.create-room-form input {
  margin-right: 10px;
  padding: 5px;
}
</style> 