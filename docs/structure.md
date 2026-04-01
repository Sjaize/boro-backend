# 프로젝트 폴더 구조

```
boro-backend/
├── app/
│   ├── api/
│   │   └── v1/               # HTTP 엔드포인트 정의 (라우터 = Controller)
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── posts.py
│   │       ├── chats.py
│   │       ├── transactions.py
│   │       └── notifications.py
│   │
│   ├── core/                 # 앱 전반에서 공유하는 핵심 설정
│   │   ├── config.py         # 환경변수 로딩 (MOCK_MODE, DB 접속 정보 등)
│   │   ├── db.py             # DB 세션 관리 (연결 열고 닫기)
│   │   ├── deps.py           # 의존성 주입 (어떤 서비스를 쓸지 결정)
│   │   └── exceptions.py     # 공통 에러 포맷 (RFC 9457)
│   │
│   ├── services/
│   │   ├── mock/             # 하드코딩된 가짜 응답 (현재 사용 중)
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── ...
│   │   └── impl/             # 실제 비즈니스 로직 (나중에 채울 곳)
│   │       ├── auth.py
│   │       ├── users.py
│   │       └── ...
│   │
│   ├── repositories/         # DB 쿼리 담당 (나중에 채울 곳)
│   ├── schemas/              # 요청/응답 타입 정의 - Pydantic (나중에 채울 곳)
│   ├── models/               # DB 테이블 정의 - SQLAlchemy ORM (팀원 작업 예정)
│   └── utils/                # 재사용 헬퍼 함수 모음
│
├── docs/                     # 팀 문서
├── main.py                   # 앱 진입점, 라우터/예외 핸들러 등록
├── requirements.txt
├── docker-compose.yaml
├── .env                      # 환경변수 (커밋 금지)
└── .env.example              # 환경변수 키 목록 (커밋용)
```

## Java Spring 대응표

| Spring | 이 프로젝트 | 현재 상태 |
|--------|------------|----------|
| Controller | `api/v1/` | 완료 |
| Service | `services/mock/` or `services/impl/` | mock 완료 |
| Repository | `repositories/` | 비어있음 |
| Entity | `models/` | 비어있음 |
| DTO | `schemas/` | 비어있음 |

## 흐름 요약

```
요청 → api/v1/ (라우터)
           ↓
       core/deps.py (MOCK_MODE 확인)
           ↓
   services/mock/      또는      services/impl/
   (가짜 응답 반환)               ↓
                            repositories/ (DB 쿼리)
                               ↓
                            models/ (ORM)
```

## MOCK_MODE 전환 방법

`.env` 파일에서 값만 바꾸면 됩니다.

```env
MOCK_MODE=true   # mock 서비스 사용 (현재)
MOCK_MODE=false  # 실제 DB 서비스 사용
```

`impl/`과 `repositories/`에 로직이 구현되어 있어야 `false`로 전환 가능합니다.
