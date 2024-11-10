# 데이터베이스 모델 설명

## 사용자 모델 (UserInDB) 

class UserInDB(BaseModel):
"""데이터베이스에 저장되는 사용자 모델"""
id: str # MongoDB ObjectId를 문자열로 저장
email: EmailStr # 이메일 주소 (로그인 식별자로 사용)
username: str # 사용자 표시 이름 (채팅방에서 표시)
hashed_password: str # bcrypt로 해시화된 비밀번호
created_at: datetime # 계정 생성 시간
is_active: bool # 계정 활성화 상태 (차단/탈퇴 관리)


## 채팅방 모델 (ChatRoom)

class ChatRoom(BaseModel):
"""채팅방 모델"""
id: Optional[str] # MongoDB ObjectId를 문자열로 저장
name: str # 채팅방 이름 (1-100자 제한)
created_by: str # 방 생성자의 username
created_at: datetime # 방 생성 시간
participants: List[str] # 참여자들의 user_id 목록



## 채팅 메시지 모델 (ChatMessageDB)
class ChatMessageDB(ChatMessageCreate):
"""데이터베이스용 채팅 메시지 모델"""
id: Optional[str] # MongoDB ObjectId를 문자열로 저장
content: str # 메시지 내용
room_id: str # 해당 메시지가 속한 채팅방 id
sender_id: str # 메시지 작성자의 user_id
created_at: datetime # 메시지 작성 시간
is_deleted: bool # 메시지 삭제 여부 (소프트 삭제)
is_system_message: bool # 시스템 메시지 여부 (입장/퇴장 등)


## 모델 설계 고려사항

1. **ID 필드**
   - MongoDB의 ObjectId를 문자열로 변환하여 저장
   - 프론트엔드와의 호환성을 위해 문자열 형태 사용

2. **시간 정보**
   - 모든 모델에 created_at 필드 포함
   - 메시지 정렬, 이력 관리, 감사 추적에 활용

3. **소프트 삭제**
   - 메시지의 경우 is_deleted 필드로 관리
   - 실제 삭제 대신 플래그로 처리하여 데이터 복구 가능

4. **관계 설정**
   - room_id, sender_id 등으로 문서 간 관계 표현
   - MongoDB의 비정규화 특성을 고려한 설계

5. **유효성 검사**
   - Pydantic 모델을 사용하여 데이터 유효성 검증
   - 이메일 형식, 문자열 길이 등 기본적인 제약 조건 설정

6. **보안**
   - 비밀번호는 해시화하여 저장
   - 민감한 정보는 별도 모델로 분리
