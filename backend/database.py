import hashlib
import os
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.models import (
    Base,
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

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "monty.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

_engine = None
_SessionFactory = None


def get_engine():
    global _engine
    if _engine is None:
        os.makedirs(DATA_DIR, exist_ok=True)
        _engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
    return _engine


def get_session() -> Session:
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine())
    return _SessionFactory()


def init_db():
    """Create all tables and seed demo data if the database is empty."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    session = get_session()
    try:
        if session.query(User).count() == 0:
            seed_demo_data(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed_demo_data(session: Session):
    """Populate the database with demo data matching the original hardcoded session state."""
    demo_user = User(
        username="demo",
        password_hash=hash_password("demo"),
        name="Demo Teacher",
        email="demo@monty.app",
        school="Montessori Academy",
        classroom="Primary",
    )
    session.add(demo_user)
    session.flush()

    # --- Settings ---
    default_settings = {
        "profile": {
            "name": "Jennifer Adams",
            "email": "jennifer.adams@montessori.edu",
            "phone": "(555) 123-4567",
            "bio": "Certified Montessori teacher with 8 years of experience in primary education.",
        },
        "classroom": {
            "school_name": "Willow Creek Montessori",
            "classroom_name": "Primary A (Ages 3-6)",
            "academic_year": "2025-2026",
            "student_count": 18,
            "assistant_teachers": ["Maria Garcia", "David Chen"],
        },
        "notifications": {
            "email_observations": True,
            "email_reports": True,
            "email_parent_communications": True,
            "push_activities": True,
            "push_schedule_changes": True,
            "weekly_digest": True,
            "reminder_time": "18:00:00",
        },
        "privacy_security": {
            "two_factor_auth": False,
            "session_timeout": 30,
            "data_export": True,
            "share_progress_with_parents": True,
            "analytics_tracking": True,
        },
        "appearance": {
            "theme": "light",
            "accent_color": "Purple",
            "font_size": "Medium",
            "compact_mode": False,
            "sidebar_collapsed": False,
        },
    }
    user_settings = UserSettings(user_id=demo_user.id, settings_json=default_settings)
    session.add(user_settings)

    # --- Students ---
    students_data = [
        {"name": "Emma Johnson", "age": 5, "interests": ["Nature", "Painting"], "allergies": ["Peanuts"], "parent_name": "Sarah Johnson", "parent_email": "sarah.j@email.com"},
        {"name": "Liam Chen", "age": 4, "interests": ["Building Blocks", "Music"], "allergies": [], "parent_name": "David Chen", "parent_email": "david.c@email.com"},
        {"name": "Olivia Martinez", "age": 6, "interests": ["Reading", "Science"], "allergies": ["Milk", "Eggs"], "parent_name": "Maria Martinez", "parent_email": "maria.m@email.com"},
        {"name": "Noah Williams", "age": 5, "interests": ["Sports", "Animals"], "allergies": [], "parent_name": "James Williams", "parent_email": "james.w@email.com"},
        {"name": "Ava Thompson", "age": 4, "interests": ["Dancing", "Art"], "allergies": ["Tree Nuts"], "parent_name": "Lisa Thompson", "parent_email": "lisa.t@email.com"},
        {"name": "Ethan Brown", "age": 6, "interests": ["Mathematics", "Puzzles"], "allergies": ["Wheat"], "parent_name": "Robert Brown", "parent_email": "robert.b@email.com"},
    ]

    student_objects = {}
    for sd in students_data:
        student = Student(
            name=sd["name"],
            age=sd["age"],
            parent_name=sd["parent_name"],
            parent_email=sd["parent_email"],
            user_id=demo_user.id,
        )
        session.add(student)
        session.flush()
        student_objects[sd["name"]] = student

        for interest in sd["interests"]:
            session.add(StudentInterest(student_id=student.id, interest=interest))
        for allergy in sd["allergies"]:
            session.add(StudentAllergy(student_id=student.id, allergy=allergy))

    # --- Schedule ---
    schedule_data = [
        {"day": "Monday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
        {"day": "Monday", "time": "9:00 AM", "activity": "Practical Life", "duration": 45, "students": "Primary A"},
        {"day": "Monday", "time": "10:00 AM", "activity": "Language Arts", "duration": 45, "students": "Primary B"},
        {"day": "Monday", "time": "11:00 AM", "activity": "Outdoor Play", "duration": 30, "students": "All"},
        {"day": "Tuesday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
        {"day": "Tuesday", "time": "9:00 AM", "activity": "Mathematics", "duration": 45, "students": "Primary A"},
        {"day": "Tuesday", "time": "10:00 AM", "activity": "Sensory Activities", "duration": 45, "students": "Primary B"},
        {"day": "Wednesday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
        {"day": "Wednesday", "time": "9:00 AM", "activity": "Art & Creativity", "duration": 60, "students": "All"},
        {"day": "Thursday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
        {"day": "Thursday", "time": "9:00 AM", "activity": "Science & Nature", "duration": 45, "students": "Primary A"},
        {"day": "Thursday", "time": "10:00 AM", "activity": "Music & Movement", "duration": 45, "students": "Primary B"},
        {"day": "Friday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
        {"day": "Friday", "time": "9:00 AM", "activity": "Free Choice Work", "duration": 60, "students": "All"},
        {"day": "Friday", "time": "11:00 AM", "activity": "Show & Tell", "duration": 30, "students": "All"},
    ]

    for sd in schedule_data:
        session.add(Schedule(
            day=sd["day"],
            time=sd["time"],
            activity=sd["activity"],
            duration=sd["duration"],
            students_group=sd["students"],
            user_id=demo_user.id,
        ))

    # --- Observations ---
    observations_data = [
        {"student": "Emma Johnson", "date": "2026-02-10", "area": "Practical Life", "notes": "Emma showed excellent concentration while working with the pouring activity. She was able to pour water from one jug to another with minimal spills.", "skills": ["Concentration", "Fine Motor"]},
        {"student": "Liam Chen", "date": "2026-02-10", "area": "Sensorial", "notes": "Liam spent 20 minutes working with the pink tower. He carefully stacked the cubes from largest to smallest, showing good visual discrimination.", "skills": ["Visual Discrimination", "Math Readiness"]},
        {"student": "Olivia Martinez", "date": "2026-02-11", "area": "Language", "notes": "Olivia is beginning to sound out CVC words using the movable alphabet. She successfully wrote 'cat', 'dog', and 'sun'.", "skills": ["Phonics", "Writing"]},
        {"student": "Noah Williams", "date": "2026-02-11", "area": "Mathematics", "notes": "Noah demonstrated understanding of number rods 1-10. He was able to count accurately and associate quantity with symbol.", "skills": ["Counting", "Quantity/Symbol"]},
        {"student": "Ava Thompson", "date": "2026-02-12", "area": "Art", "notes": "Ava enjoyed the cutting activity with scissors. She showed good control and was able to follow curved lines.", "skills": ["Fine Motor", "Hand-eye Coordination"]},
    ]

    for od in observations_data:
        student = student_objects[od["student"]]
        obs_date = date.fromisoformat(od["date"])
        obs = Observation(
            student_id=student.id,
            date=obs_date,
            area=od["area"],
            notes=od["notes"],
        )
        session.add(obs)
        session.flush()
        for skill in od["skills"]:
            session.add(ObservationSkill(observation_id=obs.id, skill=skill))

    # --- Materials ---
    materials_data = [
        {"name": "Pink Tower", "category": "Sensorial", "age_range": "3-6", "description": "Ten pink wooden cubes of varying sizes to develop visual discrimination of dimension.", "in_stock": True, "times_used": 45},
        {"name": "Brown Stairs", "category": "Sensorial", "age_range": "3-6", "description": "Ten brown wooden prisms of varying thickness to develop visual discrimination.", "in_stock": True, "times_used": 38},
        {"name": "Red Rods", "category": "Sensorial", "age_range": "3-6", "description": "Ten red wooden rods of varying length to develop visual discrimination of length.", "in_stock": True, "times_used": 32},
        {"name": "Movable Alphabet", "category": "Language", "age_range": "3-6", "description": "Set of wooden letters for building words and sentences phonetically.", "in_stock": True, "times_used": 67},
        {"name": "Number Rods", "category": "Mathematics", "age_range": "3-6", "description": "Red and blue wooden rods for learning numbers 1-10 and quantity.", "in_stock": True, "times_used": 52},
        {"name": "Sandpaper Letters", "category": "Language", "age_range": "2.5-4", "description": "Rough letters for tactile letter recognition and learning letter sounds.", "in_stock": True, "times_used": 28},
    ]

    for md in materials_data:
        session.add(Material(
            name=md["name"],
            category=md["category"],
            age_range=md["age_range"],
            description=md["description"],
            in_stock=md["in_stock"],
            times_used=md["times_used"],
            user_id=demo_user.id,
        ))
