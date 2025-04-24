# app/api/main.py

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging
from app.api.routes.router import router as api_router

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

static_dir = os.path.join(os.path.dirname(__file__), "static")

app = FastAPI()
app.include_router(api_router)
