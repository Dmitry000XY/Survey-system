from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from src.dependencies.dependencies import get_setting_service
from src.schemas.settings import SettingUpdate, SettingOut
from src.services.settings import SettingService

settings_router = APIRouter(tags=["Settings"], prefix="/settings")
setting_service = Annotated[SettingService, Depends(get_setting_service)]


@settings_router.get("/", response_model=SettingOut)
async def get_setting(service: setting_service):
    setting = await service.get_setting()
    if setting:
        return setting
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@settings_router.put("/", response_model=SettingOut)
async def update_setting(new_data: Annotated[SettingUpdate, Depends()], service: setting_service):
    updated = await service.update_setting(new_data)
    if updated:
        return updated
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@settings_router.post("/", response_model=SettingOut)
async def create_setting(new_data: Annotated[SettingUpdate, Depends()], service: setting_service):
    return await service.create_setting(new_data)


@settings_router.post("/init", response_model=SettingOut)
async def init_setting(new_data: Annotated[SettingUpdate, Depends()], service: setting_service, response: Response):
    # Вся логика инициализации перенесена в сервис: функция init_settings должна вернуть (result, created)
    result, created = await service.init_settings(new_data)
    if created:
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_200_OK
    return result
