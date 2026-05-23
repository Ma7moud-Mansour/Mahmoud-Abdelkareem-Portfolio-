from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)   # public URL or /uploads/... path
    demo_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    tags = Column(JSON, default=list)                # list of strings e.g. ["Python","FastAPI"]
    is_flagship = Column(Boolean, default=False)
    order = Column(Integer, default=0)               # display order (lower = first)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)    # "Frontend" | "Backend" | "Cloud"
    order = Column(Integer, default=0)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
