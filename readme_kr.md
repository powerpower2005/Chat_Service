# 실시간 채팅 애플리케이션 백엔드

FastAPI를 사용한 실시간 채팅 애플리케이션의 백엔드 서버

## 기술 스택

- **FastAPI**: 
- **MongoDB**: 
- **JWT**: 사용자 인증
- **Pydantic**: 데이터 검증
- **Docker**

## 주요 기능

### 사용자 관리
- 회원가입/로그인 (JWT 인증)
- 사용자 검색
- 프로필 관리

### 채팅 기능
- 실시간 1:1 및 그룹 채팅
- 채팅방 생성 및 관리 
- 채팅 이력 저장 및 조회
- 사용자 초대

## 프로젝트 구조

backend/
├── app/
│   ├── models/         # 데이터 모델
│   ├── routes/         # API 라우트
│   ├── services/       # 비즈니스 로직
│   ├── utils/          # 유틸리티 함수
│   ├── websocket/      # WebSocket 관련 코드
│   ├── middleware/     # 미들웨어
│   ├── config.py       # 설정
│   ├── database.py     # DB 연결
│   └── main.py         # 앱 시작점
└── requirements.txt    # 의존성

## 주요 API 엔드포인트

### 인증
- `POST /auth/register`: 회원가입
- `POST /auth/token`: 로그인

### 채팅
- `GET /chat/rooms`: 채팅방 목록 조회
- `POST /chat/rooms`: 채팅방 생성
- `GET /chat/rooms/{room_id}`: 채팅방 정보 조회
- `POST /chat/rooms/{room_id}/join`: 채팅방 참여
- `POST /chat/rooms/{room_id}/leave`: 채팅방 나가기
- `POST /chat/{room_id}/invite/{user_id}`: 사용자 초대

### WebSocket
- `WebSocket /ws/chat/{room_id}`: 실시간 채팅

### 사용자
- `GET /users/search`: 사용자 검색

## 환경 변수

# 서버 설정
HOST=
PORT=

# 데이터베이스 설정
MONGODB_URL=mongodb://localhost:27017
DB_NAME=chat_db

# Redis 설정
REDIS_URL=redis://localhost:6379

# JWT 설정
SECRET_KEY=example-key  # 실제 운영환경에서는 안전한 키로 변경 필요
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS 설정
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080