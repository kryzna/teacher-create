from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_user
from backend.crud import list_schedules, create_schedule, update_schedule, delete_schedule
from backend.models import User
from backend.schemas import ScheduleCreate, ScheduleUpdate, ScheduleResponse

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


@router.get("", response_model=list[ScheduleResponse])
def get_schedules(current_user: User = Depends(get_current_user)):
    return list_schedules(current_user.id)


@router.post("", response_model=ScheduleResponse, status_code=201)
def add_schedule(body: ScheduleCreate, current_user: User = Depends(get_current_user)):
    return create_schedule(current_user.id, body.model_dump())


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def edit_schedule(schedule_id: int, body: ScheduleUpdate, current_user: User = Depends(get_current_user)):
    try:
        return update_schedule(schedule_id, body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{schedule_id}", status_code=204)
def remove_schedule(schedule_id: int, current_user: User = Depends(get_current_user)):
    delete_schedule(schedule_id)
