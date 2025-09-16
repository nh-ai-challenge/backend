"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 이벤트"""
    # 시작 시
    print("Starting up...")
    print(f"API Title: {settings.PROJECT_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"API Version: {settings.API_V1_STR}")
    yield
    # 종료 시
    print("Shutting down...")


# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="NH AI Challenge - 농업 데이터 분석 및 AI 서비스 API",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
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
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])


@app.get("/", tags=["root"])
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Welcome to NH AI Challenge API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health_check": f"{settings.API_V1_STR}/health"
    }