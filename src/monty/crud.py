"""Data access layer — converts between ORM models and the dict format used by pages."""

from datetime import date as date_type

from sqlalchemy.orm import Session

from src.monty.database import get_session
from src.monty.models import (
    DailyActivity,
    DailyEntry,
    Material,
    Observation,
    ObservationSkill,
    Schedule,
    Student,
    StudentAllergy,
    StudentInterest,
    User,
    UserSettings,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _student_to_dict(s: Student) -> dict:
    return {
        "id": s.id,
        "name": s.name,
        "age": s.age,
        "interests": [i.interest for i in s.interests],
        "allergies": [a.allergy for a in s.allergies],
        "parent_name": s.parent_name or "",
        "parent_email": s.parent_email or "",
    }


def _observation_to_dict(o: Observation) -> dict:
    return {
        "id": o.id,
        "student": o.student.name,
        "date": o.date.isoformat() if isinstance(o.date, date_type) else str(o.date),
        "area": o.area,
        "notes": o.notes or "",
        "skills": [sk.skill for sk in o.skills],
    }


def _schedule_to_dict(s: Schedule) -> dict:
    return {
        "id": s.id,
        "day": s.day,
        "time": s.time,
        "activity": s.activity,
        "duration": s.duration,
        "students": s.students_group,
    }


def _material_to_dict(m: Material) -> dict:
    return {
        "id": m.id,
        "name": m.name,
        "category": m.category,
        "age_range": m.age_range or "",
        "description": m.description or "",
        "in_stock": m.in_stock,
        "times_used": m.times_used,
    }


def _daily_entry_to_dict(e: DailyEntry) -> dict:
    return {
        "id": e.id,
        "student": e.student.name,
        "date": e.date.isoformat() if isinstance(e.date, date_type) else str(e.date),
        "subject": e.subject,
        "activities": [a.activity for a in e.activities],
        "skill_level": e.skill_level,
        "notes": e.notes or "",
    }


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

def list_students(user_id: int) -> list[dict]:
    session = get_session()
    try:
        students = session.query(Student).filter_by(user_id=user_id).all()
        return [_student_to_dict(s) for s in students]
    finally:
        session.close()


def create_student(user_id: int, data: dict) -> dict:
    session = get_session()
    try:
        student = Student(
            name=data["name"],
            age=data["age"],
            parent_name=data.get("parent_name", ""),
            parent_email=data.get("parent_email", ""),
            user_id=user_id,
        )
        session.add(student)
        session.flush()
        for interest in data.get("interests", []):
            session.add(StudentInterest(student_id=student.id, interest=interest))
        for allergy in data.get("allergies", []):
            session.add(StudentAllergy(student_id=student.id, allergy=allergy))
        session.commit()
        result = _student_to_dict(student)
        return result
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_student(student_id: int, data: dict) -> dict:
    session = get_session()
    try:
        student = session.query(Student).get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")
        student.name = data["name"]
        student.age = data["age"]
        student.parent_name = data.get("parent_name", "")
        student.parent_email = data.get("parent_email", "")
        # Replace interests
        session.query(StudentInterest).filter_by(student_id=student.id).delete()
        for interest in data.get("interests", []):
            session.add(StudentInterest(student_id=student.id, interest=interest))
        # Replace allergies
        session.query(StudentAllergy).filter_by(student_id=student.id).delete()
        for allergy in data.get("allergies", []):
            session.add(StudentAllergy(student_id=student.id, allergy=allergy))
        session.commit()
        session.refresh(student)
        return _student_to_dict(student)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_student(student_id: int):
    session = get_session()
    try:
        student = session.query(Student).get(student_id)
        if student:
            session.delete(student)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Observations
# ---------------------------------------------------------------------------

def list_observations(user_id: int) -> list[dict]:
    session = get_session()
    try:
        observations = (
            session.query(Observation)
            .join(Student)
            .filter(Student.user_id == user_id)
            .all()
        )
        return [_observation_to_dict(o) for o in observations]
    finally:
        session.close()


def create_observation(user_id: int, data: dict) -> dict:
    session = get_session()
    try:
        student = session.query(Student).filter_by(name=data["student"], user_id=user_id).first()
        if not student:
            raise ValueError(f"Student '{data['student']}' not found")
        obs_date = data["date"] if isinstance(data["date"], date_type) else date_type.fromisoformat(data["date"])
        obs = Observation(
            student_id=student.id,
            date=obs_date,
            area=data["area"],
            notes=data.get("notes", ""),
        )
        session.add(obs)
        session.flush()
        for skill in data.get("skills", []):
            session.add(ObservationSkill(observation_id=obs.id, skill=skill))
        session.commit()
        return _observation_to_dict(obs)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_observation(observation_id: int, user_id: int, data: dict) -> dict:
    session = get_session()
    try:
        obs = session.query(Observation).get(observation_id)
        if not obs:
            raise ValueError(f"Observation {observation_id} not found")
        student = session.query(Student).filter_by(name=data["student"], user_id=user_id).first()
        if not student:
            raise ValueError(f"Student '{data['student']}' not found")
        obs.student_id = student.id
        obs.date = data["date"] if isinstance(data["date"], date_type) else date_type.fromisoformat(data["date"])
        obs.area = data["area"]
        obs.notes = data.get("notes", "")
        session.query(ObservationSkill).filter_by(observation_id=obs.id).delete()
        for skill in data.get("skills", []):
            session.add(ObservationSkill(observation_id=obs.id, skill=skill))
        session.commit()
        session.refresh(obs)
        return _observation_to_dict(obs)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_observation(observation_id: int):
    session = get_session()
    try:
        obs = session.query(Observation).get(observation_id)
        if obs:
            session.delete(obs)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------

def list_schedules(user_id: int) -> list[dict]:
    session = get_session()
    try:
        schedules = session.query(Schedule).filter_by(user_id=user_id).all()
        return [_schedule_to_dict(s) for s in schedules]
    finally:
        session.close()


def create_schedule(user_id: int, data: dict) -> dict:
    session = get_session()
    try:
        sched = Schedule(
            day=data["day"],
            time=data["time"],
            activity=data["activity"],
            duration=data["duration"],
            students_group=data["students"],
            user_id=user_id,
        )
        session.add(sched)
        session.commit()
        return _schedule_to_dict(sched)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_schedule(schedule_id: int, data: dict) -> dict:
    session = get_session()
    try:
        sched = session.query(Schedule).get(schedule_id)
        if not sched:
            raise ValueError(f"Schedule {schedule_id} not found")
        sched.day = data["day"]
        sched.time = data["time"]
        sched.activity = data["activity"]
        sched.duration = data["duration"]
        sched.students_group = data["students"]
        session.commit()
        return _schedule_to_dict(sched)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_schedule(schedule_id: int):
    session = get_session()
    try:
        sched = session.query(Schedule).get(schedule_id)
        if sched:
            session.delete(sched)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

def list_materials(user_id: int) -> list[dict]:
    session = get_session()
    try:
        materials = session.query(Material).filter_by(user_id=user_id).all()
        return [_material_to_dict(m) for m in materials]
    finally:
        session.close()


def create_material(user_id: int, data: dict) -> dict:
    session = get_session()
    try:
        mat = Material(
            name=data["name"],
            category=data["category"],
            age_range=data.get("age_range", ""),
            description=data.get("description", ""),
            in_stock=data.get("in_stock", True),
            times_used=data.get("times_used", 0),
            user_id=user_id,
        )
        session.add(mat)
        session.commit()
        return _material_to_dict(mat)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_material(material_id: int, data: dict) -> dict:
    session = get_session()
    try:
        mat = session.query(Material).get(material_id)
        if not mat:
            raise ValueError(f"Material {material_id} not found")
        mat.name = data["name"]
        mat.category = data["category"]
        mat.age_range = data.get("age_range", "")
        mat.description = data.get("description", "")
        mat.in_stock = data.get("in_stock", True)
        mat.times_used = data.get("times_used", 0)
        session.commit()
        return _material_to_dict(mat)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def increment_material_usage(material_id: int) -> dict:
    session = get_session()
    try:
        mat = session.query(Material).get(material_id)
        if not mat:
            raise ValueError(f"Material {material_id} not found")
        mat.times_used = (mat.times_used or 0) + 1
        session.commit()
        return _material_to_dict(mat)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_material(material_id: int):
    session = get_session()
    try:
        mat = session.query(Material).get(material_id)
        if mat:
            session.delete(mat)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Daily Entries
# ---------------------------------------------------------------------------

def list_daily_entries(user_id: int) -> list[dict]:
    session = get_session()
    try:
        entries = session.query(DailyEntry).filter_by(user_id=user_id).all()
        return [_daily_entry_to_dict(e) for e in entries]
    finally:
        session.close()


def create_daily_entry(user_id: int, data: dict) -> dict:
    session = get_session()
    try:
        student = session.query(Student).filter_by(name=data["student"], user_id=user_id).first()
        if not student:
            raise ValueError(f"Student '{data['student']}' not found")
        entry_date = data["date"] if isinstance(data["date"], date_type) else date_type.fromisoformat(data["date"])
        entry = DailyEntry(
            student_id=student.id,
            date=entry_date,
            subject=data["subject"],
            skill_level=data["skill_level"],
            notes=data.get("notes", ""),
            user_id=user_id,
        )
        session.add(entry)
        session.flush()
        for activity in data.get("activities", []):
            session.add(DailyActivity(daily_entry_id=entry.id, activity=activity))
        session.commit()
        return _daily_entry_to_dict(entry)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_daily_entry(entry_id: int, user_id: int, data: dict) -> dict:
    session = get_session()
    try:
        entry = session.query(DailyEntry).get(entry_id)
        if not entry:
            raise ValueError(f"DailyEntry {entry_id} not found")
        student = session.query(Student).filter_by(name=data["student"], user_id=user_id).first()
        if not student:
            raise ValueError(f"Student '{data['student']}' not found")
        entry.student_id = student.id
        entry.date = data["date"] if isinstance(data["date"], date_type) else date_type.fromisoformat(data["date"])
        entry.subject = data["subject"]
        entry.skill_level = data["skill_level"]
        entry.notes = data.get("notes", "")
        session.query(DailyActivity).filter_by(daily_entry_id=entry.id).delete()
        for activity in data.get("activities", []):
            session.add(DailyActivity(daily_entry_id=entry.id, activity=activity))
        session.commit()
        session.refresh(entry)
        return _daily_entry_to_dict(entry)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_daily_entry(entry_id: int):
    session = get_session()
    try:
        entry = session.query(DailyEntry).get(entry_id)
        if entry:
            session.delete(entry)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# User Settings
# ---------------------------------------------------------------------------

def get_user_settings(user_id: int) -> dict | None:
    session = get_session()
    try:
        us = session.query(UserSettings).filter_by(user_id=user_id).first()
        return us.settings_json if us else None
    finally:
        session.close()


def save_user_settings(user_id: int, settings: dict):
    session = get_session()
    try:
        us = session.query(UserSettings).filter_by(user_id=user_id).first()
        if us:
            us.settings_json = settings
        else:
            us = UserSettings(user_id=user_id, settings_json=settings)
            session.add(us)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
