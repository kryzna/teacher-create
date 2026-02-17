from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    school = Column(String(200), nullable=True)
    classroom = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    students = relationship("Student", back_populates="user", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="user", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="user", cascade="all, delete-orphan")
    daily_entries = relationship("DailyEntry", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    settings_json = Column(JSON, nullable=False, default=dict)

    user = relationship("User", back_populates="settings")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    parent_name = Column(String(200), nullable=True)
    parent_email = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="students")
    interests = relationship("StudentInterest", back_populates="student", cascade="all, delete-orphan")
    allergies = relationship("StudentAllergy", back_populates="student", cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="student", cascade="all, delete-orphan")
    daily_entries = relationship("DailyEntry", back_populates="student", cascade="all, delete-orphan")


class StudentInterest(Base):
    __tablename__ = "student_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    interest = Column(String(200), nullable=False)

    student = relationship("Student", back_populates="interests")


class StudentAllergy(Base):
    __tablename__ = "student_allergies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    allergy = Column(String(200), nullable=False)

    student = relationship("Student", back_populates="allergies")


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    area = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)

    student = relationship("Student", back_populates="observations")
    skills = relationship("ObservationSkill", back_populates="observation", cascade="all, delete-orphan")


class ObservationSkill(Base):
    __tablename__ = "observation_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    observation_id = Column(Integer, ForeignKey("observations.id"), nullable=False)
    skill = Column(String(200), nullable=False)

    observation = relationship("Observation", back_populates="skills")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)
    activity = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False)
    students_group = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="schedules")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    age_range = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    in_stock = Column(Boolean, default=True)
    times_used = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="materials")


class DailyEntry(Base):
    __tablename__ = "daily_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    subject = Column(String(100), nullable=False)
    skill_level = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="daily_entries")
    student = relationship("Student", back_populates="daily_entries")
    activities = relationship("DailyActivity", back_populates="daily_entry", cascade="all, delete-orphan")


class DailyActivity(Base):
    __tablename__ = "daily_activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_entry_id = Column(Integer, ForeignKey("daily_entries.id"), nullable=False)
    activity = Column(String(200), nullable=False)

    daily_entry = relationship("DailyEntry", back_populates="activities")
