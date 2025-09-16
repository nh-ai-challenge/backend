"""
데이터베이스 연결 및 세션 관리
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.ENVIRONMENT == "development",  # 개발 환경에서만 SQL 로그 출력
    future=True,
    poolclass=NullPool,  # 연결 풀링 비활성화 (필요시 변경)
)

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 베이스 클래스 생성 (모든 모델이 상속받을 클래스)
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    데이터베이스 세션 의존성
    FastAPI의 Depends에서 사용
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    데이터베이스 초기화
    테이블 생성 등의 작업 수행
    """
    async with engine.begin() as conn:
        # 개발 환경에서만 테이블 자동 생성
        # 프로덕션에서는 Alembic 마이그레이션 사용 권장
        if settings.ENVIRONMENT == "development":
            await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    데이터베이스 연결 종료
    """
    await engine.dispose()