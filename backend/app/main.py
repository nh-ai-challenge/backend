"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import secrets

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 이벤트"""
    print("Starting up...")
    print(f"API Title: {settings.PROJECT_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"API Version: {settings.API_V1_STR}")
    
    await init_db()
    print("Database initialized")
    
    yield
    
    print("Shutting down...")
    await close_db()
    print("Database connection closed")


# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="NH AI Challenge - 농업 데이터 분석 및 AI 서비스 API",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# 세션 미들웨어 설정 (CORS보다 먼저 추가해야 함)
app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    session_cookie="nh_session",
    max_age=3600 * 24,  # 24시간
    same_site="lax",
    https_only=False  # 개발 환경에서는 False, 프로덕션에서는 True
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(api_v1_router)


@app.get("/", tags=["root"])
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Welcome to NH AI Challenge API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health_check": f"{settings.API_V1_STR}/health"
    }