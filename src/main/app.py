from fastapi import FastAPI

from src.main.routers import api

app = FastAPI()

app.include_router(api.router)
