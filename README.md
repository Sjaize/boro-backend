# Boro Backend

## 🚀 프로젝트 소개
Boro Backend는 확장 가능한 시스템, API 설계, 데이터베이스 및 보안에 중점을 둔 백엔드 서비스입니다.

## 🛠️ 기술 스택
- **언어**: Python
- **프레임워크**: FastAPI
- **데이터베이스**: PostgreSQL
- **인프라**: Docker, AWS

## 🏁 시작하기

### 📋 사전 준비
- Docker Desktop 설치
- Python 3.9+ (Poetry 또는 Conda 환경 권장)

### ⚙️ 환경 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가합니다.
**주의**: `POSTGRES_PASSWORD`와 같은 민감한 정보는 실제 배포 환경에서 안전하게 관리해야 합니다.

```ini
{POSTGRES_USER}
{POSTGRES_PASSWORD}
{POSTGRES_DB}
{POSTGRES_HOST}
{POSTGRES_PORT}
```

### 🐳 Docker를 이용한 실행
데이터베이스 및 기타 서비스는 Docker Compose를 통해 쉽게 실행할 수 있습니다.

```bash
# 백그라운드에서 서비스 실행
docker compose up -d

# 서비스 중지 및 제거
docker compose down
```

### 🐍 로컬 개발 환경 실행
Python 환경을 활성화하고 의존성을 설치한 후 애플리케이션을 실행합니다.

```bash
# (선택 사항) Conda 환경 활성화 (기존 README 기반)
conda activate boro

# 의존성 설치 (requirements.txt 또는 poetry install 사용)
pip install -r requirements.txt
# 또는 poetry install

# FastAPI 애플리케이션 실행
uvicorn main:app --reload
```

### 📚 API 문서
애플리케이션이 실행 중일 때, 다음 주소에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.
- Swagger UI: http://localhost:8000/docs