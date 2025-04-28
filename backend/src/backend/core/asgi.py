from datetime import datetime
from fastapi.staticfiles import StaticFiles
from backend.core.exceptions import MedServiceException
from fastapi import FastAPI, Request
from backend.config import config
from backend.routes import global_router
from backend.config import config
import platform
from fastapi.middleware.cors import CORSMiddleware
from .mdns import get_local_ip

def set_exception(app: FastAPI):
    @app.exception_handler(MedServiceException)
    async def med_service_exception_handler(request: Request, exc: MedServiceException):
        return exc.to_response()

    return app


def mount_media(app: FastAPI):
    if not config.MEDIA_DIR.exists():
        config.MEDIA_DIR.mkdir(parents=False, exist_ok=True)
    app.mount("/media", StaticFiles(directory=config.MEDIA_DIR), name="media")


def helf_check(app: FastAPI):
    @app.get(config.ROUTER_GLOBAL_PREFIX + '/health')
    async def get_status():
        return {
            "status": "online",
            "serverName": platform.node(),
            "ipAddress": get_local_ip(),
            "timestamp": datetime.now().isoformat()
        }

def cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(debug=config.DEBUG)
    app.include_router(global_router)

    set_exception(app)
    mount_media(app)
    helf_check(app)
    cors(app)

    return app



app = create_app()