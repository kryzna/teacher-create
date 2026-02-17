from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_user
from backend.crud import list_observations, create_observation, update_observation, delete_observation
from backend.models import User
from backend.schemas import ObservationCreate, ObservationUpdate, ObservationResponse

router = APIRouter(prefix="/api/observations", tags=["observations"])


@router.get("", response_model=list[ObservationResponse])
def get_observations(current_user: User = Depends(get_current_user)):
    return list_observations(current_user.id)


@router.post("", response_model=ObservationResponse, status_code=201)
def add_observation(body: ObservationCreate, current_user: User = Depends(get_current_user)):
    try:
        return create_observation(current_user.id, body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{observation_id}", response_model=ObservationResponse)
def edit_observation(observation_id: int, body: ObservationUpdate, current_user: User = Depends(get_current_user)):
    try:
        return update_observation(observation_id, current_user.id, body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{observation_id}", status_code=204)
def remove_observation(observation_id: int, current_user: User = Depends(get_current_user)):
    delete_observation(observation_id)
