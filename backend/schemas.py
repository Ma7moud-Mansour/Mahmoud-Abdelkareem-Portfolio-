from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional, List, Any
from datetime import datetime


# ────────────────────────────────────────────────────────────────
# Project Schemas
# ────────────────────────────────────────────────────────────────

class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None
    tags: List[str] = []
    is_flagship: bool = False
    order: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_flagship: Optional[bool] = None
    order: Optional[int] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ────────────────────────────────────────────────────────────────
# Skill Schemas
# ────────────────────────────────────────────────────────────────

class SkillBase(BaseModel):
    name: str
    category: str   # "Frontend" | "Backend" | "Cloud"
    order: int = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    order: Optional[int] = None


class SkillResponse(SkillBase):
    id: int
    model_config = {"from_attributes": True}


# ────────────────────────────────────────────────────────────────
# Auth Schemas
# ────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
