from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import env
from app.core.endpoints import post, user


def get_application():
    _app = FastAPI(
        title="fastapi_social",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin for origin in env.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

app.include_router(user.user_router)
app.include_router(post.post_router)
