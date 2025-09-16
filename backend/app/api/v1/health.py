"""
헬스체크 엔드포인트
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, Any

from app.core.database import get_db

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    서비스 헬스체크
    """
    return {
        "status": "healthy",
        "service": "NH AI Challenge API"
    }


@router.get("/health/db")
async def database_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    데이터베이스 연결 상태 확인
    """
    try:
        # 간단한 쿼리 실행으로 DB 연결 확인
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }