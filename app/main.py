"""This module contains the app instance that is run by uvicorn."""

from fastapi import FastAPI
from app.api import routes  # use full import since app is a package

app = FastAPI()

app.include_router(routes.router)
