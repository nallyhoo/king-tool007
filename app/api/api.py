
from fastapi import APIRouter

from app.api.endpoints import processing_jobs

api_router = APIRouter()
api_router.include_router(processing_jobs.router, prefix="/jobs", tags=["jobs"])
