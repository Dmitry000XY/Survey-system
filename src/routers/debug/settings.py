from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.api.openapi import NOT_FOUND_RESPONSE
from src.dependencies import get_setting_service
from src.schemas.settings import SettingOut, SettingUpdate
from src.services.settings import SettingService

settings_router = APIRouter(tags=["Settings"], prefix="/settings")
SettingServiceDependency = Annotated[SettingService, Depends(get_setting_service)]


@settings_router.get("", response_model=SettingOut, status_code=status.HTTP_200_OK, responses=NOT_FOUND_RESPONSE)
async def get_setting(service: SettingServiceDependency) -> SettingOut:
    return await service.get_setting()


@settings_router.patch("", response_model=SettingOut, status_code=status.HTTP_200_OK, responses=NOT_FOUND_RESPONSE)
async def update_setting(new_data: SettingUpdate, service: SettingServiceDependency) -> SettingOut:
    return await service.update_setting(new_data)


@settings_router.put(
    "",
    response_model=SettingOut,
    status_code=status.HTTP_200_OK,
    responses={
        201: {
            "model": SettingOut,
            "description": "Settings were created",
        }
    },
)
async def ensure_settings(service: SettingServiceDependency, response: Response) -> SettingOut:
    setting, created = await service.ensure_settings()
    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return setting
