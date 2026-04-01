from fastapi import FastAPI

from app.api.v1 import router as v1_router
from app.core.exceptions import AppError, app_error_handler

app = FastAPI(
    title="Boro API",
    version="0.1.0",
    docs_url="/swagger-ui/index.html",
    redoc_url="/redoc",
)

app.add_exception_handler(AppError, app_error_handler)
app.include_router(v1_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
