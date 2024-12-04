from fastapi import APIRouter

from app.routers.v1 import inference as v1_inference
from app.routers.v1 import reception as v1_reception

api_router = APIRouter()
api_router.include_router(v1_reception.router, prefix="/v1")
api_router.include_router(v1_inference.router, prefix="/v1")
