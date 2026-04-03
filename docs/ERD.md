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
    users ||--o{ user_device_tokens : has

    posts ||--o{ post_images : has
    posts ||--o{ post_likes : liked_by
    posts ||--o{ chat_rooms : starts
    posts ||--o{ transactions : results_in

    chat_rooms ||--o{ chat_room_participants : includes
    chat_rooms ||--o{ chat_messages : contains
    chat_rooms ||--o| transactions : linked_to

    transactions ||--o{ reviews : has

    users {
        bigint id PK "User PK"
        string nickname "Nickname"
        string profile_image_url "Profile image URL"
        string region_name "Region name"
        decimal current_lat "Current latitude"
        decimal current_lng "Current longitude"
        datetime location_updated_at "Last location update time"
        int notification_radius_m "Alert radius in meters"
        boolean nearby_urgent_alerts_enabled "Nearby urgent alerts opt-in"
        int completed_transaction_count "Completed transaction count"
        decimal trust_score "Average trust score"
        string status "User status (active, banned)"
        datetime created_at "Created at"
        datetime updated_at "Updated at"
        datetime last_login_at "Last login time"
    }

    user_interest_keywords {
        bigint id PK "PK"
        bigint user_id FK "User ID / UNIQUE(user_id, keyword)"
        string keyword "Interest keyword"
        datetime created_at "Created at"
    }

    social_accounts {
        bigint id PK "PK"
        bigint user_id FK "User ID"
        string provider "Provider (google, kakao)"
        string provider_user_id "Provider user ID / UNIQUE(provider, provider_user_id)"
        string provider_email "Provider email"
        string provider_name "Provider name"
        string provider_profile_image_url "Provider profile image URL"
        datetime created_at "Created at"
        datetime updated_at "Updated at"
    }

    posts {
        bigint id PK "Post PK"
        bigint user_id FK "Author user ID"
        string post_type "Post type (LEND, BORROW)"
        string title "Title"
        text content "Content"
        int price "Price"
        boolean is_urgent "Urgent flag"
        string category "Category"
        string rental_period_text "Rental period text"
        string meeting_place_text "Meeting place text"
        string region_name "Region name"
        decimal lat "Latitude"
        decimal lng "Longitude"
        int chat_count "Chat count cache"
        int like_count "Like count cache"
        string status "Post status"
        datetime created_at "Created at"
        datetime updated_at "Updated at"
    }

    post_images {
        bigint id PK "PK"
        bigint post_id FK "Post ID"
        string image_url "Image URL"
        int sort_order "Image sort order"
        datetime created_at "Created at"
    }

    post_likes {
        bigint id PK "PK"
        bigint user_id FK "User ID / UNIQUE(user_id, post_id)"
        bigint post_id FK "Post ID / UNIQUE(user_id, post_id)"
        datetime created_at "Created at"
    }

    chat_rooms {
        bigint id PK "PK"
        bigint post_id FK "Post ID"
        bigint created_by_user_id FK "Created by user / UNIQUE(post_id, created_by_user_id)"
        string last_message_preview "Last message preview"
        datetime last_message_at "Last message time"
        datetime created_at "Created at"
    }

    chat_room_participants {
        bigint id PK "PK"
        bigint chat_room_id FK "Chat room ID / UNIQUE(chat_room_id, user_id)"
        bigint user_id FK "User ID / UNIQUE(chat_room_id, user_id)"
        string role "Role"
        bigint last_read_message_id "Last read message ID"
        int unread_count "Unread count"
        datetime joined_at "Joined at"
    }

    chat_messages {
        bigint id PK "PK"
        bigint chat_room_id FK "Chat room ID"
        bigint sender_user_id FK "Sender user ID"
        string message_type "Message type (text, image)"
        text content "Content"
        datetime created_at "Created at"
    }

    transactions {
        bigint id PK "PK"
        bigint post_id FK "Post ID"
        bigint chat_room_id FK "Chat room ID / UNIQUE(chat_room_id)"
        bigint lender_user_id FK "Lender user ID"
        bigint borrower_user_id FK "Borrower user ID"
        datetime completed_at "Completed at"
    }

    reviews {
        bigint id PK "PK"
        bigint transaction_id FK "Transaction ID / UNIQUE(transaction_id, reviewer_user_id)"
        bigint reviewer_user_id FK "Reviewer user ID / UNIQUE(transaction_id, reviewer_user_id)"
        bigint reviewee_user_id FK "Reviewee user ID"
        int rating "Rating"
        text comment "Comment"
        string[] tags "Review tags"
        datetime created_at "Created at"
    }

    notifications {
        bigint id PK "PK"
        bigint user_id FK "Recipient user ID"
        string type "Type (urgent_post, chat_message, interest_post)"
        string title "Title"
        text body "Body"
        bigint related_post_id "Related post ID (nullable, no FK constraint)"
        bigint related_chat_room_id "Related chat room ID (nullable, no FK constraint)"
        boolean is_read "Read flag"
        datetime created_at "Created at"
    }

    user_device_tokens {
        bigint id PK "PK"
        bigint user_id FK "User ID"
        string device_token "Device token / UNIQUE(device_token)"
        string platform "Platform (android, ios, web)"
        boolean is_active "Active token flag"
        datetime created_at "Created at"
        datetime updated_at "Updated at"
        datetime last_seen_at "Last seen at"
    }
