from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import auth, chat, users
from .services.chat_service import ChatService
from .services.user_service import UserService
from .middleware.error_handler import error_handler
from .config import settings
from .routes.websocket import router as websocket_router

app = FastAPI(
    title="Real-time Chat Application",
    debug=True  # Use only in development environment
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_settings.origins,
    #allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

chat_service = ChatService()
user_service = UserService()

# Add middleware
app.middleware("http")(error_handler)

# Base route
@app.get("/")
async def root():
    return {"message": "Server is running"}

app.include_router(websocket_router)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(users.router, prefix="/users", tags=["users"])