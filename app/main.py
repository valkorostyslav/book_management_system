from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app.api.routers.auth_router import router as auth_router
from app.api.routers.author_router import router as author_router
from app.api.routers.book_router import router as book_router
from app.api.routers.user_router import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/jwt/create")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(book_router, prefix="/book", tags=["Book"])
app.include_router(author_router, prefix="/author", tags=["Author"])


def custom_openapi():
    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title="My FastAPI App",
        version="1.0.0",
        description="A FastAPI application with JWT Bearer authorization",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter Bearer token as `Bearer <your_token>`",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    return openapi_schema


app.openapi = custom_openapi
