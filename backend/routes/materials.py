from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_user
from backend.crud import list_materials, create_material, update_material, increment_material_usage, delete_material
from backend.models import User
from backend.schemas import MaterialCreate, MaterialUpdate, MaterialResponse

router = APIRouter(prefix="/api/materials", tags=["materials"])


@router.get("", response_model=list[MaterialResponse])
def get_materials(current_user: User = Depends(get_current_user)):
    return list_materials(current_user.id)


@router.post("", response_model=MaterialResponse, status_code=201)
def add_material(body: MaterialCreate, current_user: User = Depends(get_current_user)):
    return create_material(current_user.id, body.model_dump())


@router.put("/{material_id}", response_model=MaterialResponse)
def edit_material(material_id: int, body: MaterialUpdate, current_user: User = Depends(get_current_user)):
    try:
        return update_material(material_id, body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{material_id}/use", response_model=MaterialResponse)
def use_material(material_id: int, current_user: User = Depends(get_current_user)):
    try:
        return increment_material_usage(material_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{material_id}", status_code=204)
def remove_material(material_id: int, current_user: User = Depends(get_current_user)):
    delete_material(material_id)
