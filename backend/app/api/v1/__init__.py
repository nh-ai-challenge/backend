from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.surveys import router as surveys_router
from app.api.v1.matches import router as matches_router
from app.api.v1.profiles import router as profiles_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(surveys_router)
api_v1_router.include_router(matches_router)
api_v1_router.include_router(profiles_router)