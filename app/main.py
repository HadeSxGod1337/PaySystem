from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import admin, auth, users, webhook
from app.exceptions import BaseAppException

app = FastAPI(
    title="Payment System API", description="REST API для системы платежей", version="1.0.0"
)


@app.exception_handler(BaseAppException)
async def app_exception_handler(_request: Request, exc: BaseAppException) -> JSONResponse:
    """Custom application exceptions handler"""
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=headers
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP exceptions handler (including errors from OAuth2PasswordBearer)"""
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers
    )


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(webhook.router, prefix="/api/v1", tags=["webhook"])


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Payment System API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "ok"}
