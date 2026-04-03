import uuid

import boto3
from fastapi import APIRouter, Depends, Query

from app.core.config import settings
from app.core.deps import get_current_user
from app.schemas.common import DataResponse
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/api/images", tags=["Images"])


class PresignedUrlResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "upload_url": "https://s3.ap-northeast-2.amazonaws.com/boro-images/...",
                "image_url": "https://boro-images.s3.ap-northeast-2.amazonaws.com/posts/uuid.jpg",
            }
        }
    )
    upload_url: str
    image_url: str


@router.get(
    "/presigned-url",
    response_model=DataResponse[PresignedUrlResponse],
    summary="이미지 업로드용 Presigned URL 발급",
    description=(
        "S3에 이미지를 직접 업로드하기 위한 임시 URL을 발급합니다.\n\n"
        "**사용 흐름:**\n"
        "1. 이 API로 `upload_url`과 `image_url`을 받습니다.\n"
        "2. `upload_url`로 이미지 파일을 `PUT` 요청으로 업로드합니다. (Content-Type: image/jpeg)\n"
        "3. `image_url`을 게시글/프로필 등의 이미지 URL로 저장합니다.\n\n"
        "**folder 파라미터:**\n"
        "- `posts`: 게시글 이미지\n"
        "- `profiles`: 프로필 이미지\n\n"
        "Presigned URL 유효시간은 **5분**입니다."
    ),
)
async def get_presigned_url(
    folder: str = Query("posts", description="업로드 폴더 (posts, profiles)"),
    current_user: dict = Depends(get_current_user),
):
    s3 = boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    key = f"{folder}/{uuid.uuid4()}.jpg"

    upload_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.AWS_S3_BUCKET,
            "Key": key,
            "ContentType": "image/jpeg",
        },
        ExpiresIn=300,  # 5분
    )

    image_url = f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

    return {"data": {"upload_url": upload_url, "image_url": image_url}}
