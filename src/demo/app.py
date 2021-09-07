from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .accounts import api as accounts_api
from .config import settings


app = FastAPI()
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')
accounts_api.initialize_app(app)
