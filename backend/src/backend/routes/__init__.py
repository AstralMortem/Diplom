from fastapi import APIRouter
from backend.config import config
from .v1 import v1_router

global_router = APIRouter(prefix=config.ROUTER_GLOBAL_PREFIX)
global_router.include_router(v1_router)
