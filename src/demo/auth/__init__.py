from fastapi import FastAPI

from .api import router


def initialize_app(app: FastAPI):
    app.include_router(router)
