from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.configurations import close_database, close_wp_database, global_init, wp_global_init
from src.extras.synchronization_runner import start_synchronization, stop_synchronization
from src.routers import debug_router, openapi_tags


@asynccontextmanager
async def lifespan(app: FastAPI):
    global_init()
    wp_global_init()
    synchronization_task = start_synchronization()
    try:
        yield
    finally:
        await stop_synchronization(synchronization_task)
        await close_wp_database()
        await close_database()


def create_application():
    return FastAPI(
        title="Survey system",
        description="The Influenza Research Institute Survey System is a dedicated platform designed to streamline the collection of user-reported data.",
        version="0.0.1",
        # responses={404: {"description": "Not Found!"}}, # TODO
        lifespan=lifespan,
        openapi_tags=openapi_tags,
    )


app = create_application()


def _configure():
    app.include_router(debug_router)


_configure()
