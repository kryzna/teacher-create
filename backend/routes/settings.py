from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.crud import get_user_settings, save_user_settings
from backend.models import User
from backend.schemas import SettingsResponse, SettingsUpdate

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=SettingsResponse)
def get_settings(current_user: User = Depends(get_current_user)):
    settings = get_user_settings(current_user.id)
    return SettingsResponse(settings=settings or {})


@router.put("", response_model=SettingsResponse)
def update_settings(body: SettingsUpdate, current_user: User = Depends(get_current_user)):
    save_user_settings(current_user.id, body.settings)
    return SettingsResponse(settings=body.settings)
