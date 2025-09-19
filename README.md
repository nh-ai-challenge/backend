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
- **AI/ML**: Sentence-Transformers, Google Gemini API
- **Embeddings**: Korean SBERT (jhgan/ko-sroberta-multitask)

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
pip install -r backend/requirements.txt

# PyTorch 설치 (CPU 버전)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 또는 GPU 버전 (CUDA 11.8)
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### 5. 환경 변수 설정

루트 디렉토리에 `.env` 파일을 생성합니다 (backend 폴더가 아닌 프로젝트 루트):

```bash
# .env.example 복사
cp .env.example .env

# 또는 직접 생성
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:nh-challenge@localhost:5432/nh_challenge

# Gemini API (AI 매칭 설명 생성)
GEMINI_API_KEY=your_gemini_api_key_here

# External APIs (Optional)
FARMMAP_SERVICE_KEY=your_farmmap_key
FARMMAP_ENCODED_KEY=your_farmmap_encoded_key
SENTINEL_CLIENT_ID=your_sentinel_client_id
SENTINEL_CLIENT_SECRET=your_client_secret
EOF
```

### 6. 데이터베이스 초기화

```bash
cd backend

# 방법 1: 수동 마이그레이션 스크립트 (권장)
python init_migration.py

# 방법 2: Alembic 마이그레이션
alembic upgrade head

# 테이블 생성 확인
psql -U postgres -d nh_challenge -c "\dt"
```

예상되는 테이블 목록:
- users (사용자 정보)
- senior_profiles_v2 (시니어 프로필 + AI 임베딩)
- youth_profiles_v2 (청년 프로필 + AI 임베딩)
- matches (매칭 결과)
- match_requests (매칭 요청)
- matching_scores (매칭 점수)

### 7. 서버 실행
```bash
# 개발 서버 실행 (자동 리로드)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 또는 Python 모듈로 실행
python -m uvicorn app.main:app --reload
```

서버는 http://localhost:8000 에서 실행됩니다.
API 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다.

### 8. API 엔드포인트 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 헬스체크: http://localhost:8000/api/v1/health
- DB 연결 테스트: http://localhost:8000/api/v1/health/db

### 9. 주요 API 엔드포인트

#### 인증
- `POST /api/v1/auth/register` - 회원가입
- `POST /api/v1/auth/login` - 로그인
- `GET /api/v1/auth/me` - 현재 사용자 정보

#### 프로필 (AI 임베딩)
- `GET /api/v1/profiles/me` - 내 프로필 조회
- `PUT /api/v1/profiles/me/profile-text` - 프로필 텍스트 업데이트 (자동 임베딩 생성)

#### 설문
- `POST /api/v1/surveys/senior` - 시니어 설문 제출
- `POST /api/v1/surveys/youth` - 청년 설문 제출
- `GET /api/v1/surveys/senior/profile` - 시니어 프로필 조회
- `GET /api/v1/surveys/youth/profile` - 청년 프로필 조회

#### AI 하이브리드 매칭
- `GET /api/v1/matches/recommendations/hybrid` - AI 하이브리드 매칭 추천
- `GET /api/v1/matches/{id}?generate_explanation=true` - 매칭 상세 + AI 설명
- `POST /api/v1/matches/calculate` - 매칭 점수 계산

## AI 매칭 시스템 아키텍처

### 하이브리드 매칭 엔진
1. **텍스트 임베딩 (30%)**
   - 한국어 SBERT 모델 사용 (jhgan/ko-sroberta-multitask)
   - 768차원 벡터로 프로필 텍스트 인코딩
   - 코사인 유사도로 의미적 매칭

2. **SCI 점수 (70%)**
   - 농업 철학 (40%)
   - 사업 운영 (20%)
   - 멘토십 (20%)
   - 재무 조건 (20%)

3. **2단계 필터링**
   - 1차: 임베딩 유사도 필터 (상위 후보 선별)
   - 2차: 상세 SCI 점수 계산 (최종 순위)

### Gemini AI 통합
- 매칭 이유를 한국어 자연어로 설명
- 프로필 데이터 기반 구조화된 분석
- 매칭 강점, 주의사항, 성공 가능성 제시

## 테스트 데이터 생성

```bash
cd backend
python scripts/generate_test_data.py --seniors 100 --youths 100
```

이 스크립트는:
- 다양한 페르소나의 시니어/청년 사용자 생성
- 프로필 텍스트 자동 생성 및 임베딩 계산
- 실제 같은 설문 응답 시뮬레이션

## 트러블슈팅

### Python 3.13 호환성 문제
Python 3.13 사용시 SQLAlchemy 비동기 기능 오류가 발생할 수 있습니다.
```bash
pip install greenlet==3.1.1
```

### 임베딩 모델 다운로드 오류
```bash
# 모델 수동 다운로드
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('jhgan/ko-sroberta-multitask')"
```

### Gemini API 오류
- API 키 확인: https://makersuite.google.com/app/apikey
- 환경 변수 확인: `echo $GEMINI_API_KEY`
- Rate limit 확인 (무료 tier: 60 requests/minute)

### PostgreSQL 연결 오류
```bash
# PostgreSQL 서비스 상태 확인
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql      # Linux

# 서비스 재시작
brew services restart postgresql@16   # macOS
sudo systemctl restart postgresql     # Linux
```

### 메모리 부족 오류 (임베딩 모델)
```bash
# CPU 전용 PyTorch 설치로 메모리 사용량 감소
pip uninstall torch torchvision torchaudio
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## 성능 최적화 팁

1. **임베딩 캐싱**: 프로필 텍스트 변경 시에만 재계산
2. **배치 처리**: 여러 텍스트 동시 임베딩 생성
3. **인덱싱**: embedding_updated_at 필드에 인덱스 추가
4. **연결 풀**: PostgreSQL 연결 풀 크기 조정

## 개발 환경 권장사항

- Python 3.9 이상 (3.11 권장)
- PostgreSQL 14 이상
- RAM 8GB 이상 (임베딩 모델용)
- SSD 스토리지 (모델 로딩 속도)
