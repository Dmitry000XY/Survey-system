from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.configurations import create_db_and_tables, delete_db_and_tables, global_init, wp_global_init
from src.routers import debug_router, openapi_tags


@asynccontextmanager
async def lifespan(app: FastAPI):
    global_init()
    wp_global_init()
    await create_db_and_tables()
    yield
    # await delete_db_and_tables()  # TODO


def create_application():
    return FastAPI(
        title="Survey system",
        description="The Influenza Research Institute Survey System is a dedicated platform designed to streamline the collection of user-reported data.",
        version="0.0.1",
        # responses={404: {"description": "Not Found!"}}, # TODO
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        openapi_tags=openapi_tags
    )


app = create_application()


def _configure():
    app.include_router(debug_router)


_configure()
