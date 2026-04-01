# 팀 개발 컨벤션

## 브랜치 전략

`main` → `develop` → `feature/*` / `fix/*` / `chore/*` 구조를 따릅니다.

```
main        ← 프로덕션 배포 브랜치. 직접 push 금지.
develop     ← 개발 통합 브랜치. PR을 통해서만 merge.
feature/*   ← 기능 개발
fix/*       ← 버그 수정
chore/*     ← 설정, 의존성, 문서 등 코드 변경 없는 작업
refactor/*  ← 리팩토링
```

### 브랜치 네이밍

```
feature/post-list-api
feature/auth-oauth-kakao
fix/chat-unread-count
chore/swagger-setup
refactor/user-service-layer
```

- 소문자 + 하이픈 사용
- 작업 내용이 명확하게 드러나도록 작성

---

## 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 스타일을 따릅니다.

### 형식

```
<type>: <제목>

[본문 - 선택]
```

### type 목록

| type | 설명 |
|------|------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `refactor` | 기능 변화 없는 코드 개선 |
| `chore` | 설정, 패키지, 문서 등 |
| `test` | 테스트 추가/수정 |
| `style` | 포맷, 세미콜론 등 코드 의미 변화 없음 |
| `docs` | 문서 작성/수정 |

### 예시

```
feat: 게시글 목록 조회 API 구현

fix: 채팅방 안 읽은 메시지 수 초기화 오류 수정

chore: Swagger 경로 /swagger-ui/index.html 로 변경

refactor: UserService 인터페이스/구현체 분리

docs: API 응답 포맷 컨벤션 문서 추가
```

- 제목은 50자 이내, 명령형 동사로 작성 (예: "추가", "수정", "변경")
- 마침표 붙이지 않음
- 본문이 필요한 경우 제목과 한 줄 띄우고 작성

---

## PR (Pull Request)

### 규칙

- `develop` 브랜치로만 PR 생성 (main 직접 PR 금지)
- PR 하나는 하나의 작업 단위
- 머지 전 최소 1명 코드 리뷰 승인 필요
- 머지 방식: **Squash and Merge** (커밋 히스토리 정리)

### PR 제목

커밋 메시지와 동일한 형식 사용

```
feat: 게시글 작성 API 구현
fix: 로그인 토큰 만료 처리 오류 수정
```

### PR 본문 템플릿

```markdown
## 작업 내용
- 

## 변경 사항
- 

## 참고 사항 (선택)
- 
```

---

## API 응답 포맷

### 성공

```json
{
  "data": { }
}
```

### 에러 (RFC 9457)

```json
{
  "type": "https://api.boro.com/errors/POST_NOT_FOUND",
  "title": "Not Found",
  "status": 404,
  "detail": "게시글을 찾을 수 없습니다.",
  "instance": "/api/posts/123",
  "code": "POST_NOT_FOUND",
  "timestamp": "2026-03-30T12:34:56Z"
}
```

---

## 코드 스타일

- Python 포매터: **black**, 린터: **ruff**
- 들여쓰기: 스페이스 4칸
- 변수/함수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- 파일명: `snake_case.py`

### import 순서

```python
# 1. 표준 라이브러리
from datetime import datetime

# 2. 서드파티
from fastapi import APIRouter, Depends

# 3. 내부 모듈
from app.core.deps import get_current_user
from app.schemas.posts import PostResponse
```

---

## 환경변수

- `.env` 파일은 절대 커밋하지 않음 (`.gitignore` 등록 필수)
- `.env.example` 파일에 키 목록만 유지 (값 없이)
- 새 환경변수 추가 시 `.env.example`도 함께 업데이트
