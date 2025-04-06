from fastapi.staticfiles import StaticFiles
from backend.core.exceptions import MedServiceException
from fastapi import FastAPI, Request
from backend.config import config
from backend.routes import global_router
from backend.config import config

def set_exception(app: FastAPI):
    
    @app.exception_handler(MedServiceException)
    async def med_service_exception_handler(request: Request, exc: MedServiceException):
        return exc.to_response()

    return app


def mount_media(app: FastAPI):
    app.mount("/media", StaticFiles(directory=config.MEDIA_DIR), name="media")


def create_app() -> FastAPI:
    app = FastAPI(debug=config.DEBUG)
    app.include_router(global_router)

    set_exception(app)
    mount_media(app)

    return app
