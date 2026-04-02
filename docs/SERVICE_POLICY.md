# Service Policy

- 이 문서는 서비스 전제와 개발 중 임시 운영 규칙을 정리한다.
- API 계약 자체는 [API_SPEC.md](./API_SPEC.md)를 기준으로 본다.

## App Scope

- 본 서비스는 앱 중심 서비스이며, 주요 상호작용은 로그인 이후 사용을 기본 전제로 한다.
- 다만 목록/검색처럼 일부 조회 API는 확장 가능성을 고려해 비인증으로 유지할 수 있다.

## Posts Policy

- `GET /api/posts`는 목록/검색 조회 API로 인증 없이 호출할 수 있다.
- `GET /api/posts/{post_id}`와 게시글 작성/수정/삭제, 좋아요, 채팅방 생성은 인증이 필요한 보호 API로 본다.
- 게시글 상세 응답에는 `is_liked_by_me` 같은 사용자 문맥이 포함될 수 있으므로 인증 전제를 유지한다.

## Development Auth

- auth/JWT API 완성 전 non-mock 환경에서는 `X-User-Id` 헤더로 보호 API를 테스트한다.
- 최종 배포 기준 인증 방식은 `Authorization: Bearer <access_token>`이다.
