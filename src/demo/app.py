from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import accounts
from . import auth
from .config import settings


app = FastAPI()
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')

accounts.initialize_app(app)
auth.initialize_app(app)
