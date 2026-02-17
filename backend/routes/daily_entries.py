from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_user
from backend.crud import list_daily_entries, create_daily_entry, update_daily_entry, delete_daily_entry
from backend.models import User
from backend.schemas import DailyEntryCreate, DailyEntryUpdate, DailyEntryResponse

router = APIRouter(prefix="/api/daily-entries", tags=["daily-entries"])


@router.get("", response_model=list[DailyEntryResponse])
def get_daily_entries(current_user: User = Depends(get_current_user)):
    return list_daily_entries(current_user.id)


@router.post("", response_model=DailyEntryResponse, status_code=201)
def add_daily_entry(body: DailyEntryCreate, current_user: User = Depends(get_current_user)):
    try:
        return create_daily_entry(current_user.id, body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{entry_id}", response_model=DailyEntryResponse)
def edit_daily_entry(entry_id: int, body: DailyEntryUpdate, current_user: User = Depends(get_current_user)):
    try:
        return update_daily_entry(entry_id, current_user.id, body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{entry_id}", status_code=204)
def remove_daily_entry(entry_id: int, current_user: User = Depends(get_current_user)):
    delete_daily_entry(entry_id)
