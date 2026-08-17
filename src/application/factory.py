from fastapi import FastAPI

from src.api import register_exception_handlers
from src.configurations import get_settings
from src.routers import debug_router, openapi_tags

from .lifespan import lifespan


def create_application() -> FastAPI:
    application = FastAPI(
        title="Survey system",
        description=(
            "The Influenza Research Institute Survey System is a dedicated platform designed to streamline "
            "the collection of user-reported data."
        ),
        version="0.1.0",
        lifespan=lifespan,
        openapi_tags=openapi_tags,
    )

    register_exception_handlers(application)
    if get_settings().ENABLE_DEBUG_API:
        application.include_router(debug_router)

    return application
