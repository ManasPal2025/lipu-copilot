"""Versioned API router composition."""

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.organizations import router as organizations_router
from app.api.v1.product_catalog import router as product_catalog_router
from app.api.v1.quotes import router as quotes_router
from app.api.v1.users import router as users_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(organizations_router)
api_router.include_router(product_catalog_router)
api_router.include_router(quotes_router)
api_router.include_router(users_router)
