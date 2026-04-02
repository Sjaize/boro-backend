erDiagram
    users ||--o{ social_accounts : has
    users ||--o{ posts : writes
    users ||--o{ post_likes : likes
    users ||--o{ chat_room_participants : joins
    users ||--o{ chat_messages : sends
    users ||--o{ transactions : lends
    users ||--o{ transactions : borrows
    users ||--o{ reviews : writes
    users ||--o{ reviews : receives
    users ||--o{ notifications : receives
    users ||--o{ user_interest_keywords : has

    posts ||--o{ post_images : has
    posts ||--o{ post_likes : liked_by
    posts ||--o{ chat_rooms : starts
    posts ||--o| transactions : results_in

    chat_rooms ||--o{ chat_room_participants : includes
    chat_rooms ||--o{ chat_messages : contains
    chat_rooms ||--o| transactions : linked_to
    chat_rooms ||--o{ notifications : related_to

    transactions ||--o{ reviews : has

    users{
        bigint id PK "유저 PK"
        string nickname "닉네임"
        string profile_image_url "프로필 사진"
        string region_name "지역"
        decimal current_lat "위도"
        decimal current_lng "경도"
        int notification_radius_m "알림 반경(m)"
        int completed_transaction_count "거래 완료 횟수"
        decimal trust_score "평균 별점"
        string status "유저 상태(active, banned 등)"
        datetime created_at "생성일"
        datetime updated_at "수정일"
        datetime last_login_at "마지막 로그인"
    }

    user_interest_keywords{
        bigint id PK "PK"
        bigint user_id FK "유저 / UNIQUE(user_id, keyword)"
        string keyword "관심 키워드"
        datetime created_at "생성일"
    }

    social_accounts{
        bigint id PK "PK"
        bigint user_id FK "유저 ID"
        string provider "로그인 제공자(google, kakao 등)"
        string provider_user_id "소셜 고유 ID / UNIQUE(provider, provider_user_id)"
        string provider_email "소셜 이메일"
        string provider_name "소셜 이름"
        string provider_profile_image_url "소셜 프로필"
        datetime created_at "생성일"
        datetime updated_at "수정일"
    }

    posts {
        bigint id PK "게시글 PK"
        bigint user_id FK "작성자"
        string post_type "빌려주세요 / 빌려드릴게요"
        string title "제목"
        text content "본문"
        int price "가격"
        boolean is_urgent "긴급 여부"
        string category "카테고리"
        string rental_period_text "대여 기간"
        string meeting_place_text "거래 장소"
        string region_name "지역"
        decimal lat "위도"
        decimal lng "경도"
        int chat_count "채팅 수(캐시)"
        int like_count "좋아요 수(캐시)"
        string status "게시글 상태"
        datetime created_at "생성일"
        datetime updated_at "수정일"
    }

    post_images {
        bigint id PK "PK"
        bigint post_id FK "게시글 ID"
        string image_url "이미지 URL"
        int sort_order "이미지 순서"
        datetime created_at "생성일"
    }

    post_likes {
        bigint id PK "PK"
        bigint user_id FK "유저 / UNIQUE(user_id, post_id)"
        bigint post_id FK "게시글 / UNIQUE(user_id, post_id)"
        datetime created_at "생성일"
    }

    chat_rooms{
        bigint id PK "PK"
        bigint post_id FK "게시글"
        bigint created_by_user_id FK "채팅 건 유저 / UNIQUE(post_id, created_by_user_id)"
        
        string last_message_preview "마지막 메시지"
        datetime last_message_at "마지막 시간"
        datetime created_at "생성일"
    }

    chat_room_participants {
        bigint id PK "PK"
        bigint chat_room_id FK "채팅방 / UNIQUE(chat_room_id, user_id)"
        bigint user_id FK "유저 / UNIQUE(chat_room_id, user_id)"
        string role "역할"
        bigint last_read_message_id "마지막 읽은 메시지"
        int unread_count "안 읽은 수"
        datetime joined_at "참여 시각"
    }

    chat_messages{
        bigint id PK "PK"
        bigint chat_room_id FK "채팅방"
        bigint sender_user_id FK "보낸 사람"
        string message_type "메시지 타입(text/image)"
        text content "내용"
        datetime created_at "생성 시각"
    }

    transactions{
        bigint id PK "PK"
        bigint post_id FK "게시글"
        bigint chat_room_id FK "채팅방 / UNIQUE(chat_room_id)"
        bigint lender_user_id FK "빌려준 사람"
        bigint borrower_user_id FK "빌린 사람"
        datetime completed_at "거래 완료 시각"
    }

    reviews {
        bigint id PK "PK"
        bigint transaction_id FK "거래 / UNIQUE(transaction_id, reviewer_user_id)"
        bigint reviewer_user_id FK "평가자 / UNIQUE(transaction_id, reviewer_user_id)"
        bigint reviewee_user_id FK "평가 대상"
        int rating "별점"
        text comment "리뷰 내용"
        string[] tags "매너 평가 태그 코드 목록 (복수 선택 가능, 최대 N개)"
        datetime created_at "생성일"
    }

    notifications{
        bigint id PK "PK"
        bigint user_id FK "알림 수신자"
        string type "알림 타입(urgent_post / chat_message / interest_post)"
        string title "제목"
        text body "내용"
        bigint related_post_id "관련 게시글 (nullable, FK 제약 없음)"
        bigint related_chat_room_id "관련 채팅방 (nullable, FK 제약 없음)"
        boolean is_read "읽음 여부"
        datetime created_at "생성일"
    }