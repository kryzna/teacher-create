from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_user
from backend.crud import list_students, create_student, update_student, delete_student
from backend.models import User
from backend.schemas import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("", response_model=list[StudentResponse])
def get_students(current_user: User = Depends(get_current_user)):
    return list_students(current_user.id)


@router.post("", response_model=StudentResponse, status_code=201)
def add_student(body: StudentCreate, current_user: User = Depends(get_current_user)):
    return create_student(current_user.id, body.model_dump())


@router.put("/{student_id}", response_model=StudentResponse)
def edit_student(student_id: int, body: StudentUpdate, current_user: User = Depends(get_current_user)):
    try:
        return update_student(student_id, body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{student_id}", status_code=204)
def remove_student(student_id: int, current_user: User = Depends(get_current_user)):
    delete_student(student_id)
