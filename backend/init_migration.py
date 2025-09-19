"""
수동 마이그레이션 스크립트
기존 테이블이 있으면 그대로 사용하고, 없으면 생성
"""

from sqlalchemy import create_engine, text
from app.core.database import Base
from app.models.user import User
from app.models.profile import SeniorProfile, YouthProfile, YouthVisionProfile
from app.models.matching import Match, MatchRequest, MatchingScore

DATABASE_URL = "postgresql://postgres:nh-challenge@localhost/nh_challenge"

def init_database():
    engine = create_engine(DATABASE_URL)
    
    # 테이블 생성 (이미 있으면 무시)
    Base.metadata.create_all(bind=engine, checkfirst=True)
    
    # Alembic 버전 테이블 생성
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            )
        """))
        
        # 초기 버전 설정
        conn.execute(text("""
            INSERT INTO alembic_version (version_num) 
            VALUES ('initial_setup')
            ON CONFLICT (version_num) DO NOTHING
        """))
        conn.commit()
    
    print("생성성공")
    
    # 테이블 목록 출력
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """))
        
        print("\n📋 Current tables:")
        for row in result:
            print(f"  - {row[0]}")

if __name__ == "__main__":
    init_database()