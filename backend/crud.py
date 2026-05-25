from sqlalchemy.orm import Session
from models import Project, Skill, AdminUser
from schemas import ProjectCreate, ProjectUpdate, SkillCreate, SkillUpdate
from typing import List, Optional
import bcrypt

def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def _verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ────────────────────────────────────────────────────────────────
# Project CRUD
# ────────────────────────────────────────────────────────────────

def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).order_by(Project.is_flagship.desc(), Project.order).offset(skip).limit(limit).all()


def get_featured_projects(db: Session) -> List[Project]:
    return db.query(Project).filter(Project.is_featured == True).order_by(Project.is_flagship.desc(), Project.order).all()


def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Optional[Project]:
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    db_project = get_project(db, project_id)
    if not db_project:
        return False
    db.delete(db_project)
    db.commit()
    return True


# ────────────────────────────────────────────────────────────────
# Skill CRUD
# ────────────────────────────────────────────────────────────────

def get_skills(db: Session) -> List[Skill]:
    return db.query(Skill).order_by(Skill.category, Skill.order).all()


def get_skill(db: Session, skill_id: int) -> Optional[Skill]:
    return db.query(Skill).filter(Skill.id == skill_id).first()


def create_skill(db: Session, skill: SkillCreate) -> Skill:
    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def update_skill(db: Session, skill_id: int, skill: SkillUpdate) -> Optional[Skill]:
    db_skill = get_skill(db, skill_id)
    if not db_skill:
        return None
    update_data = skill.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_skill, key, value)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def delete_skill(db: Session, skill_id: int) -> bool:
    db_skill = get_skill(db, skill_id)
    if not db_skill:
        return False
    db.delete(db_skill)
    db.commit()
    return True


# ────────────────────────────────────────────────────────────────
# Admin User CRUD
# ────────────────────────────────────────────────────────────────

def get_admin_by_username(db: Session, username: str) -> Optional[AdminUser]:
    return db.query(AdminUser).filter(AdminUser.username == username).first()


def create_admin(db: Session, username: str, password: str) -> AdminUser:
    hashed = _hash_password(password)
    user = AdminUser(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain: str, hashed: str) -> bool:
    return _verify_password(plain, hashed)


def change_admin_password(db: Session, username: str, new_password: str) -> bool:
    user = get_admin_by_username(db, username)
    if not user:
        return False
    user.hashed_password = _hash_password(new_password)
    db.commit()
    return True
