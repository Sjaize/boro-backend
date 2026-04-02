```markdown
✅ 공통 응답 포맷 (Success Response)
성공적인 API 응답은 다음 형식을 따릅니다.

{
  "data": {
    /* 응답 데이터 */
  }
}

❌ 에러 응답 포맷 (Error Response)
에러 발생 시 RFC 9457 Problem Details 형식을 기반으로 응답합니다.

{
  "type": "https://api.your-service.com/errors/{error_code}",
  "title": "Not Found",
  "status": 404,
  "detail": "게시글을 찾을 수 없습니다.",
  "instance": "/api/posts/123",
  "code": "POST_NOT_FOUND",
  "timestamp": "2026-03-30T12:34:56Z"
}
```

공통 에러 타입

| **Code** | **HTTP** | **Description** |
| --- | --- | --- |
| INVALID_TOKEN | 401 | 유효하지 않은 토큰 |
| EXPIRED_TOKEN | 401 | 만료된 토큰 |
| FORBIDDEN | 403 | 권한 없음 |
| NOT_FOUND | 404 | 리소스를 찾을 수 없음 |
| CONFLICT | 409 | 리소스 충돌 |
| BAD_REQUEST | 400 | 잘못된 요청 |
| INTERNAL_SERVER_ERROR | 500 | 서버 오류 |

### Auth

| Method | Endpoint | Description | Request | Response |
| --- | --- | --- | --- | --- |
| POST | /api/auth/oauth/{provider} | 소셜 로그인 및 회원가입 | { "access_token": "string" } | { "data": { "access_token": "string", "refresh_token": "string", "is_new_user": boolean } } |
| POST | /api/auth/refresh | Access Token 재발급 | { "refresh_token": "string" } | { "data": { "access_token": "string" } } |
| POST | /api/auth/logout | 로그아웃 | { "refresh_token": "string" } | { "data": null } |
| DELETE | /api/auth/withdrawal | 회원탈퇴 | 없음 (Authorization 헤더 사용) | { "data": null } |

### Users

- 회원 가입 직후 정보 입력받는 페이지 필요?
- 지역은 회원가입할 때 받는 값..? 지금 위치 값인가요..?
- 마이페이지의 관심 키워드 등록 화면 그려주세요
- 거래 상세 보기 페이지 아직 안 그려짐

| Method | Endpoint | Description | Request | Response |
| --- | --- | --- | --- | --- |
| GET | /api/users/me | 내 프로필 및 마이페이지 요약 정보 조회 (닉네임, 프로필 이미지, 동네, 신뢰도, 빌린 횟수, 빌려준 횟수, 관심목록의 개수) | 없음 (Authorization 헤더 ****사용) | { "data": { "id": 1, "nickname": "홍길동", "profile_image_url": "https://...", "region_name": "영통동", "trust_score": 4.8, "borrow_count": 3, "lend_count": 5, "like_count": 12 } } |
| PATCH | /api/users/me | 내 프로필 수정 (닉네임, 프로필 이미지) | { "nickname": "새닉네임", "profile_image_url": "https://..." } | { "data": { "id": 1, "nickname": "새닉네임", "profile_image_url": "https://..." } } |
| PUT | /api/users/me/location | 현재 위치 업데이트 및 동네명 갱신 (lat/lng 기반 reverse geocoding 수행) | { "lat": 37.123, "lng": 127.123 } | { "data": { "region_name": "강남구", "full_address": "서울특별시 강남구 역삼동", "lat": 37.123, "lng": 127.123 } } |
| PATCH | /api/users/me/settings | 사용자 설정 변경 (알림 반경, 관심 키워드 / 일부 필드만 전송 가능) | { "notification_radius_m": 1500, "interest_keywords": ["전자기기", "가구"] } | { "data": { "notification_radius_m": 1500, "interest_keywords": ["전자기기", "가구"] } } |
| GET | /api/users/{user_id} | 타 유저 프로필 조회 (닉네임, 프로필 이미지, 동네, 신뢰도, 거래 완료 횟수, 리뷰 수 등 공개 정보) | 없음 | { "data": { "id": 2, "nickname": "유저2", "profile_image_url": "https://...", "region_name": "영통동", "completed_transaction_count": 10, "trust_score": 4.7, "review_count": 8 } } |
| GET | /api/users/{user_id}/reviews | 특정 유저가 받은 리뷰 목록 조회 | query: { page: 1, size: 10 } | { "data": { "reviews": [ { "review_id": 1, "rating": 5, "comment": "좋아요!", "created_at": "2026-03-30T12:34:56Z" } ], "page": 1, "size": 10, "has_next": false } } |
| GET | /api/users/me/posts | 내가 작성한 게시글 목록 조회 | query: { post_type: "borrow" | "lend", page: 1, size: 10 } | { "data": { "posts": [ { "post_id": 1, "title": "보조배터리 구해요", "post_type": "borrow", "price": 1100, "region_name": "영통동", "like_count": 3, "chat_count": 2, "status": "active", "created_at": "2026-03-30T12:34:56Z" } ], "page": 1, "size": 10, "has_next": true } } |
| GET | /api/users/{user_id}/posts | 특정 유저가 작성한 게시글 목록 조회 | query: { post_type: "borrow" | "lend", page: 1, size: 10 } | { "data": { "posts": [ { "post_id": 2, "title": "우산 빌려드려요", "post_type": "lend", "price": 2000, "region_name": "영통동", "like_count": 5, "chat_count": 1, "status": "active", "created_at": "2026-03-30T12:34:56Z" } ], "page": 1, "size": 10, "has_next": false } } |
| GET | /api/users/me/likes | 내가 관심 등록한 게시글 목록 조회 | query: { page: 1, size: 10 } | { "data": { "posts": [ { "post_id": 2, "title": "우산 빌려드려요", "post_type": "lend", "price": 2000, "region_name": "영통동", "like_count": 5, "chat_count": 1, "status": "active", "created_at": "2026-03-30T12:34:56Z" } ], "page": 1, "size": 10, "has_next": true } } |

### Posts

#### 인증 메모

- `GET /api/posts`는 인증 없이 호출 가능
- `GET /api/posts/{post_id}`와 게시글 작성/수정/삭제, 좋아요, 채팅방 생성 API는 인증 필요
- auth/JWT API 완성 전 non-mock 환경에서는 보호 API 테스트 시 `X-User-Id` 헤더를 임시로 사용
- 최종 배포 기준 인증 방식은 `Authorization: Bearer <access_token>`

| Method | Endpoint | Description | Request | Response |
| --- | --- | --- | --- | --- |
| GET | /api/posts | 게시물 목록/검색 조회 (query: keyword, post_type, category, is_urgent, region_name, page, size, sort 등) | query: { keyword: "드릴", post_type: "LEND", category: "공구", is_urgent: false, region_name: "역삼동", page: 1, size: 20, sort: "created_at" } | { "data": { "posts":[ { "post_id": 1, "title": "전동 드릴 빌려드려요", "post_type": "LEND", "price": 5000, "region_name": "역삼동", "is_urgent": false, "thumbnail_url": "https://example.com/thumb.jpg", "like_count": 5, "chat_count": 2, "status": "AVAILABLE", "created_at": "2026-03-31T09:00:00" } ], "page": 1, "size": 20, "has_next": true } } |
| POST | /api/posts | 게시글 작성 | { "post_type": "LEND", "title": "전동 드릴 빌려드려요", "content": "거의 새거입니다.", "price": 5000, "category": "공구", "is_urgent": false, "rental_period_text": "1일 기준", "region_name": "역삼동", "lat": 37.5006, "lng": 127.0364, "image_urls":[ "https://example.com/img1.jpg", "https://example.com/img2.jpg" ] }
 | { "data": { "post_id": 1 } } |
| GET | /api/posts/{post_id} | 게시글 상세 조회(가격, 시간, 거래희망장소)
 | 없음 | { "data": { "post_id": 1, "author": { "user_id": 42, "nickname": "동네주민", "profile_image_url": "[**https://example.com/profile.jpg**](https://www.google.com/url?sa=E&q=https%3A%2F%2Fexample.com%2Fprofile.jpg)", "trust_score": 4.8 }, "post_type": "LEND", "title": "전동 드릴 빌려드려요", "content": "거의 새거입니다.", "price": 5000, "category": "공구", "is_urgent": false, "rental_period_text": "1일 기준", "meeting_place_text": "역삼역 3번 출구", "region_name": "역삼동", "lat": 37.5006, "lng": 127.0364, "images":[ { "image_url": "https://example.com/img1.jpg", "sort_order": 1 } ], "like_count": 5, "chat_count": 2, "status": "AVAILABLE", "is_liked_by_me": true, "created_at": "2026-03-31T09:00:00" } } |
| PATCH | /api/posts/{post_id} | 게시글 수정 | { "title": "전동 드릴 빌려드려요(가격인하)", "price": 4000, "content": "가격 내렸습니다.", "status": "RESERVED", "image_urls":[ "https://example.com/img1.jpg", "https://example.com/img3.jpg" ] } | { "data": { "post_id": 1 } } |
| DELETE | /api/posts/{post_id} | 게시글 삭제 | 없음 | { "data": { "post_id": 1, "deleted": true } } |
| POST | /api/posts/{post_id}/likes | 게시물에 관심 등록하기 | 없음 | { "data": { "post_id": 1, "like_count": 6, "is_liked": true } } |
| DELETE | /api/posts/{post_id}/likes | 게시물 관심 등록 해제하기 | 없음 | { "data": { "post_id": 1, "like_count": 5, "is_liked": false } } |
| POST  | /api/posts/{post_id}/chats | 채팅방 생성 또는 기존 채팅방 반환 | 없음 | { "data": { "chat_room_id": 12, "is_new": true } } |

### Chats

| Method | Endpoint | Description | Request | Response |
| --- | --- | --- | --- | --- |
| GET | /api/chats | 내 채팅방 목록 조회 | query: { type: "ALL" | "BORROW" | "LEND", page: 1, size: 20 } | { "data": { "chat_rooms": [ { "chat_room_id": 55, "post_id": 101, "post_type": "BORROW", "post_title": "보조배터리 구해요", "partner_nickname": "닉네임", "partner_profile_image_url": "https://example.com/profile.jpg", "last_message_preview": "보조배터리 필요하시는 글 보고 연락드렸어요", "last_message_at": "2026-03-30T09:39:00", "unread_count": 3 } ], "page": 1, "size": 20, "has_next": true } } |
| GET | /api/chats/{chat_room_id} | 채팅방 상세 조회 (게시글 정보, 참여자 정보, 마지막 읽은 메시지, 안 읽은 메시지 수, 거래 완료 여부 포함) | 없음 | { "data": { "chat_room_id": 55, "post": { "post_id": 101, "title": "보조배터리 구해요", "price": 1100, "rental_period_text": "1시간", "post_image_url": "https://example.com/post1.jpg", "post_type": "BORROW" }, "participants": [ { "user_id": 1, "nickname": "나", "profile_image_url": "https://example.com/me.jpg", "role": "borrower" }, { "user_id": 2, "nickname": "닉네임", "profile_image_url": "https://example.com/profile.jpg", "role": "lender" } ], "last_read_message_id": 203, "unread_count": 3, "transaction_completed": false } } |
| GET | /api/chats/{chat_room_id}/messages | 채팅 메시지 내역 조회 (cursor pagination) | query: { cursor: message_id, size: 20 } | { "data": { "messages": [ { "message_id": 201, "sender_user_id": 1, "message_type": "text", "content": "텍스트가 들어갈 공간입니다", "created_at": "2026-03-30T15:58:00", "is_mine": true }, { "message_id": 202, "sender_user_id": 2, "message_type": "text", "content": "음", "created_at": "2026-03-30T15:59:00", "is_mine": false } ], "next_cursor": 180, "has_next": true } } |
| POST | /api/chats/{chat_room_id}/messages | 메시지 전송 | { "message_type": "text", "content": "안녕하세요!" } | { "data": { "message_id": 205, "chat_room_id": 55, "sender_user_id": 1, "message_type": "text", "content": "안녕하세요!", "created_at": "2026-03-30T16:02:00", "is_mine": true } } |
| PATCH | /api/chats/{chat_room_id}/read | 채팅방 읽음 처리 (마지막 읽은 메시지 갱신, 안 읽은 메시지 수 초기화) | { "last_read_message_id": 205 } | { "data": { "chat_room_id": 55, "last_read_message_id": 205, "unread_count": 0 } } |

### transactions

| Method | Endpoint | Description | Request | Response |
| --- | --- | --- | --- | --- |
| GET | /api/transactions | 내 거래내역 목록 조회 | query: { role: "borrower" | "lender", page: 1, size: 10 } | { "data": { "transactions": [ { "transaction_id": 1, "post_id": 101, "chat_room_id": 55, "role": "borrower", "post_title": "보조배터리 구해요", "post_image_url": "https://example.com/post1.jpg", "price": 1100, "rental_period_text": "1시간", "chat_count": 0, "like_count": 0, "completed_at": "2026-03-30T09:41:00", "review": { "has_received_review": true } }, { "transaction_id": 2, "post_id": 102, "chat_room_id": 56, "role": "borrower", "post_title": "우산 구해요", "post_image_url": "https://example.com/post2.jpg", "price": 2000, "rental_period_text": "반나절", "chat_count": 1, "like_count": 2, "completed_at": "2026-03-30T09:36:00", "review": { "has_received_review": false } } ], "page": 1, "size": 10, "has_next": true } } |
| POST | /api/transactions | 거래 완료 기록 생성 (생성 시 양측 유저의 거래 횟수 및 게시글 상태 함께 갱신) | { "post_id": 101, "chat_room_id": 55 } | { "data": { "transaction_id": 1, "post_id": 101, "chat_room_id": 55, "lender_user_id": 2, "borrower_user_id": 1, "completed_at": "2026-03-30T09:41:00" } } |
| GET | /api/transactions/{transaction_id} | 거래 상세 조회 | 없음 | { "data": { "transaction_id": 1, "post_id": 101, "chat_room_id": 55, "lender_user_id": 2, "borrower_user_id": 1, "my_role": "borrower", "completed_at": "2026-03-30T09:41:00", "post": { "title": "보조배터리 구해요", "content": "1시간 정도 빌리고 싶어요.", "price": 1100, "category": "전자기기", "rental_period_text": "1시간", "meeting_place_text": "경희대 국제캠 정문 앞", "region_name": "영통동", "post_image_urls": [ "https://example.com/post1.jpg" ], "chat_count": 0, "like_count": 0 }, "review": { "has_received_review": true, "rating": 5, "comment": "시간 약속 잘 지켜주셨어요.", "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"] } } } |
| POST | /api/transactions/{transaction_id}/reviews | 거래에 대한 리뷰 작성 (거래 참여자 각각 1회 작성 가능, reviewer/reviewee는 서버에서 자동 결정) | { "rating": 5, "comment": "시간 약속 잘 지켜주셨어요.", "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"] } | { "data": { "review_id": 1, "transaction_id": 1, "rating": 5, "comment": "시간 약속 잘 지켜주셨어요.", "tags": ["KEEPS_PROMISES", "KIND_AND_POLITE"], "created_at": "2026-03-30T10:00:00" } } |

### Notifications

- 이전
    
    
    | Method | Endpoint | Description | Request | Response |
    | --- | --- | --- | --- | --- |
    | GET | /api/notifications | 내 알림 목록 조회
    최신순 정렬, 페이징 지원 |  | {
      "data": {
        "notifications": [
          {
            "id": 1,
            "type": "urgent_post",
            "title": "주변에 물건이 필요한 사람이 있어요!",
            "body": "보조배터리 필요해요",
            "related_post_id": 101,
            "related_chat_room_id": null,
            "is_read": false,
            "created_at": "2026-03-30T09:39:00"
          },
          {
            "id": 2,
            "type": "interest_post",
            "title": "관심 키워드 등록한 물건 게시글이 올라왔어요!",
            "body": "보조배터리 빌려드려요",
            "related_post_id": 102,
            "related_chat_room_id": null,
            "is_read": false,
            "created_at": "2026-03-30T09:35:00"
          },
          {
            "id": 3,
            "type": "chat_message",
            "title": "새로운 채팅 메시지가 도착했어요!",
            "body": "오늘 6시에 거래 가능하신가요?",
            "related_post_id": 101,
            "related_chat_room_id": 55,
            "is_read": true,
            "created_at": "2026-03-30T09:20:00"
          }
        ]
      }
    } |
    | PATCH | /api/notifications/{notification_id}/read | 특정 알림 읽음 처리 |  | { "data": { "notification_id": 3, "type": "chat_message", "is_read": true }} |

| Method | Endpoint | Description | Request | Response |
| --- | --- | --- | --- | --- |
| GET | /api/notifications | 내 알림 목록 조회 (최신순 정렬, 페이징 지원) | query: { page: 1, size: 20 } | { "data": { "notifications": [ { "id": 1, "type": "urgent_post", "title": "주변에 물건이 필요한 사람이 있어요!", "body": "보조배터리 필요해요", "related_post_id": 101, "related_chat_room_id": null, "is_read": false, "created_at": "2026-03-30T09:39:00" }, { "id": 2, "type": "interest_post", "title": "관심 키워드 등록한 물건 게시글이 올라왔어요!", "body": "보조배터리 빌려드려요", "related_post_id": 102, "related_chat_room_id": null, "is_read": false, "created_at": "2026-03-30T09:35:00" }, { "id": 3, "type": "chat_message", "title": "새로운 채팅 메시지가 도착했어요!", "body": "오늘 6시에 거래 가능하신가요?", "related_post_id": 101, "related_chat_room_id": 55, "is_read": true, "created_at": "2026-03-30T09:20:00" } ], "page": 1, "size": 20, "has_next": true } } |
| PATCH | /api/notifications/{notification_id}/read | 특정 알림 읽음 처리 | 없음 | { "data": { "id": 3, "is_read": true } } |

### Notification Type

- urgent_post: 긴급 요청 게시글 알림
- interest_post: 관심 키워드 기반 게시글 알림
- chat_message: 채팅 메시지 알림

### Field Notes

- id: 알림 ID
- related_post_id: 게시글 관련 알림일 경우 사용
- related_chat_room_id: 채팅 알림일 경우 사용
- created_at: 알림 생성 시각
- is_read: 읽음 여부
