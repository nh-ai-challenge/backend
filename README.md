# NH AI Challenge Backend

농업 데이터 분석 및 AI 서비스를 위한 FastAPI 백엔드 서버

## 프로젝트 구조

```
backend/
├── app/                    # 메인 애플리케이션
│   ├── __init__.py
│   ├── main.py            # FastAPI 앱 진입점
│   ├── api/               # API 엔드포인트
│   │   ├── __init__.py
│   │   └── v1/            # API 버전 1
│   │       └── __init__.py
│   ├── core/              # 핵심 설정 및 유틸리티
│   │   ├── __init__.py
│   │   ├── config.py      # 환경 설정
│   │   └── database.py    # 데이터베이스 연결
│   ├── models/            # SQLAlchemy 데이터베이스 모델
│   │   └── __init__.py
│   ├── schemas/           # Pydantic 스키마 (요청/응답 모델)
│   │   └── __init__.py
│   ├── services/          # 비즈니스 로직
│   │   └── __init__.py
│   └── utils/             # 공통 유틸리티 함수
│       └── __init__.py
├── alembic/               # 데이터베이스 마이그레이션
├── tests/                 # 테스트 코드
│   └── __init__.py
├── scripts/               # 유틸리티 스크립트
├── sentinel_farm_analysis/ # Sentinel 위성 데이터 분석 (기존)
│   ├── test_response.py
│   └── test_2024_data.json
├── requirements.txt       # 프로젝트 의존성
├── .env                  # 환경 변수 (Git에서 제외)
├── .gitignore           # Git 제외 파일
├── main.py              # PyCharm 템플릿 (제거 예정)
├── test_farm_api.py     # 팜맵 API 테스트 (기존)
└── test_farmmap_api.py  # 팜맵 API 테스트 (기존)
```

## 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migration**: Alembic
- **ASGI Server**: Uvicorn
- **Testing**: Pytest

## 주요 기능

- 농업 기상 데이터 조회 (공공데이터포털 API 연동)
- Sentinel 위성 영상 분석 (NDVI 등 식생 지수)
- PostgreSQL 데이터베이스 연동
- RESTful API 제공

## 설치 및 실행

### 1. PostgreSQL 설치 및 설정

#### macOS
```bash
# PostgreSQL 설치
brew install postgresql@16
brew services start postgresql@16

# 데이터베이스 및 사용자 생성
psql -d postgres
CREATE USER postgres WITH PASSWORD 'nh-challenge' CREATEDB;
CREATE DATABASE nh_challenge OWNER postgres;
\q
```

#### Ubuntu/Debian
```bash
# PostgreSQL 설치
sudo apt update
sudo apt install postgresql postgresql-contrib

# 데이터베이스 및 사용자 생성
sudo -u postgres psql
CREATE USER postgres WITH PASSWORD 'nh-challenge' CREATEDB;
CREATE DATABASE nh_challenge OWNER postgres;
\q
```

### 2. 프로젝트 클론 및 이동
```bash
git clone https://github.com/nh-ai-challenge/backend.git
cd backend
```

### 3. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 4. 의존성 설치
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. 환경 변수 설정
`.env` 파일을 생성하고 필요한 환경 변수를 설정합니다:
```bash
# .env 파일 생성
cat > .env << EOF
# PostgreSQL Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=nh-challenge
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nh_challenge

# API Keys (선택사항 - 외부 API 사용시)
FARMMAP_SERVICE_KEY=your_key
FARMMAP_ENCODED_KEY=your_encoded_key
SENTINEL_CLIENT_ID=your_client_id
SENTINEL_CLIENT_SECRET=your_client_secret
EOF
```

### 6. 서버 실행
```bash
# 개발 서버 실행 (자동 리로드)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 또는 Python 모듈로 실행
python -m uvicorn app.main:app --reload
```

서버는 http://localhost:8000 에서 실행됩니다.
API 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다.

### 7. API 엔드포인트 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 헬스체크: http://localhost:8000/api/v1/health
- DB 연결 테스트: http://localhost:8000/api/v1/health/db

## 트러블슈팅

### Python 3.13 호환성 문제
Python 3.13 사용시 SQLAlchemy 비동기 기능 오류가 발생할 수 있습니다.
```bash
pip install greenlet==3.1.1
```

### PostgreSQL 연결 오류
```bash
# PostgreSQL 서비스 상태 확인
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql      # Linux

# 서비스 재시작
brew services restart postgresql@16   # macOS
sudo systemctl restart postgresql     # Linux
```