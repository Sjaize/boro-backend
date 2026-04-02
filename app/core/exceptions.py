from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, status: int, code: str, title: str, detail: str):
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail
        super().__init__(detail)


class InvalidTokenError(AppError):
    def __init__(self):
        super().__init__(401, "INVALID_TOKEN", "Unauthorized", "유효하지 않은 토큰입니다.")


class ExpiredTokenError(AppError):
    def __init__(self):
        super().__init__(401, "EXPIRED_TOKEN", "Unauthorized", "만료된 토큰입니다.")


class ForbiddenError(AppError):
    def __init__(self, detail: str = "접근 권한이 없습니다."):
        super().__init__(403, "FORBIDDEN", "Forbidden", detail)


class NotFoundError(AppError):
    def __init__(self, detail: str = "리소스를 찾을 수 없습니다."):
        super().__init__(404, "NOT_FOUND", "Not Found", detail)


class ConflictError(AppError):
    def __init__(self, detail: str = "리소스 충돌이 발생했습니다."):
        super().__init__(409, "CONFLICT", "Conflict", detail)


class BadRequestError(AppError):
    def __init__(self, detail: str = "잘못된 요청입니다."):
        super().__init__(400, "BAD_REQUEST", "Bad Request", detail)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={
            "type": f"https://api.boro.com/errors/{exc.code}",
            "title": exc.title,
            "status": exc.status,
            "detail": exc.detail,
            "instance": request.url.path,
            "code": exc.code,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    )
