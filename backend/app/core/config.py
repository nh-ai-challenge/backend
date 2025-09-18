"""
애플리케이션 설정 관리
"""
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
import os
from pathlib import Path


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 프로젝트 정보
    PROJECT_NAME: str = "NH AI Challenge API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 데이터베이스
    DATABASE_URL: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", "http://localhost:8000"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return []
    
    # 외부 API 키 (기존 프로젝트)
    FARMMAP_SERVICE_KEY: Optional[str] = None
    FARMMAP_ENCODED_KEY: Optional[str] = None
    SENTINEL_CLIENT_ID: Optional[str] = None
    SENTINEL_CLIENT_SECRET: Optional[str] = None
    
    # AI 서비스 API 키
    GEMINI_API_KEY: Optional[str] = None
    
    class Config:
        # .env 파일 경로 설정
        env_file = Path(__file__).parent.parent.parent.parent / ".env"  # 루트의 .env
        env_file_encoding = "utf-8"
        case_sensitive = True


# 설정 인스턴스 생성
settings = Settings()