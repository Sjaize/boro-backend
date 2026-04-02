# Boro Backend

## 기술 스택
- **언어**: Python
- **프레임워크**: FastAPI
- **데이터베이스**: PostgreSQL
- **인프라**: Docker

## 사전 준비
- Docker Desktop 설치
- Conda 설치

## 최초 세팅 (클론 후 1회만)

### 1. 환경변수 설정
`.env.example`을 복사해 `.env` 파일을 생성합니다.

```bash
cp .env.example .env
```

### 2. Conda 환경 생성 및 의존성 설치

```bash
conda create -n boro python=3.12
conda activate boro
pip install -r requirements.txt
```

### 3. DB 초기화

```bash
docker compose up -d
alembic upgrade head
```

> `alembic upgrade head`는 DB 테이블을 생성합니다. 최초 1회 또는 migration 파일이 추가됐을 때 실행합니다.

---

## 서버 시작

```bash
conda activate boro
docker compose up -d
uvicorn main:app --reload --port 8080
```

## 서버 종료

```bash
# 터미널에서 Ctrl + C
docker compose down
conda deactivate
```

## API 문서 (Swagger)

서버 실행 후 아래 주소에서 확인:

```
http://localhost:8080/swagger-ui/index.html
```