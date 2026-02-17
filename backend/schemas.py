from pydantic import BaseModel
from typing import Any


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    school: str | None = None
    classroom: str | None = None


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

class StudentCreate(BaseModel):
    name: str
    age: int
    interests: list[str] = []
    allergies: list[str] = []
    parent_name: str = ""
    parent_email: str = ""


class StudentUpdate(StudentCreate):
    pass


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    interests: list[str] = []
    allergies: list[str] = []
    parent_name: str = ""
    parent_email: str = ""


# ---------------------------------------------------------------------------
# Observations
# ---------------------------------------------------------------------------

class ObservationCreate(BaseModel):
    student: str
    date: str
    area: str
    skills: list[str] = []
    notes: str = ""


class ObservationUpdate(ObservationCreate):
    pass


class ObservationResponse(BaseModel):
    id: int
    student: str
    date: str
    area: str
    skills: list[str] = []
    notes: str = ""


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------

class ScheduleCreate(BaseModel):
    day: str
    time: str
    activity: str
    duration: int
    students: str


class ScheduleUpdate(ScheduleCreate):
    pass


class ScheduleResponse(BaseModel):
    id: int
    day: str
    time: str
    activity: str
    duration: int
    students: str


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

class MaterialCreate(BaseModel):
    name: str
    category: str
    age_range: str = ""
    description: str = ""
    in_stock: bool = True


class MaterialUpdate(BaseModel):
    name: str
    category: str
    age_range: str = ""
    description: str = ""
    in_stock: bool = True
    times_used: int = 0


class MaterialResponse(BaseModel):
    id: int
    name: str
    category: str
    age_range: str = ""
    description: str = ""
    in_stock: bool = True
    times_used: int = 0


# ---------------------------------------------------------------------------
# Daily Entries
# ---------------------------------------------------------------------------

class DailyEntryCreate(BaseModel):
    student: str
    date: str
    subject: str
    activities: list[str] = []
    skill_level: str
    notes: str = ""


class DailyEntryUpdate(DailyEntryCreate):
    pass


class DailyEntryResponse(BaseModel):
    id: int
    student: str
    date: str
    subject: str
    activities: list[str] = []
    skill_level: str
    notes: str = ""


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

class SettingsResponse(BaseModel):
    settings: dict[str, Any]


class SettingsUpdate(BaseModel):
    settings: dict[str, Any]


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
