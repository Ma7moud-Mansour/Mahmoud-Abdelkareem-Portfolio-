import os
import uuid
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

import models
import crud
import schemas
from database import engine, get_db
from auth import settings, create_access_token, verify_token

# ────────────────────────────────────────────────────────────────
# App Setup
# ────────────────────────────────────────────────────────────────

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio API",
    description="Backend for Mahmoud Abdelkareem's portfolio",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads folder — one level up from backend/
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Frontend dir (used at bottom for static mount)
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


# ────────────────────────────────────────────────────────────────
# Seed default admin on first run
# ────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        existing = crud.get_admin_by_username(db, settings.ADMIN_USERNAME)
        if not existing:
            crud.create_admin(db, settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
            print(f"[STARTUP] Created admin user: {settings.ADMIN_USERNAME}")
    finally:
        db.close()


# ────────────────────────────────────────────────────────────────
# Auth Endpoints
# ────────────────────────────────────────────────────────────────

@app.post("/api/auth/login", response_model=schemas.TokenResponse, tags=["Auth"])
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_admin_by_username(db, payload.username)
    if not user or not crud.verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/auth/change-password", tags=["Auth"])
def change_password(
    payload: schemas.ChangePasswordRequest,
    username: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    user = crud.get_admin_by_username(db, username)
    if not user or not crud.verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    crud.change_admin_password(db, username, payload.new_password)
    return {"message": "Password changed successfully"}


@app.get("/api/auth/me", tags=["Auth"])
def me(username: str = Depends(verify_token)):
    return {"username": username}


# ────────────────────────────────────────────────────────────────
# Public: Projects
# ────────────────────────────────────────────────────────────────

@app.get("/api/projects", response_model=List[schemas.ProjectResponse], tags=["Projects"])
def get_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)


@app.get("/api/projects/featured", response_model=List[schemas.ProjectResponse], tags=["Projects"])
def get_featured_projects(db: Session = Depends(get_db)):
    return crud.get_featured_projects(db)


@app.get("/api/projects/{project_id}", response_model=schemas.ProjectResponse, tags=["Projects"])
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# ────────────────────────────────────────────────────────────────
# Public: Skills
# ────────────────────────────────────────────────────────────────

@app.get("/api/skills", response_model=List[schemas.SkillResponse], tags=["Skills"])
def get_skills(db: Session = Depends(get_db)):
    return crud.get_skills(db)


# ────────────────────────────────────────────────────────────────
# Admin: Projects
# ────────────────────────────────────────────────────────────────

@app.post("/api/admin/projects", response_model=schemas.ProjectResponse, tags=["Admin"])
def admin_create_project(
    project: schemas.ProjectCreate,
    _: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return crud.create_project(db, project)


@app.put("/api/admin/projects/{project_id}", response_model=schemas.ProjectResponse, tags=["Admin"])
def admin_update_project(
    project_id: int,
    project: schemas.ProjectUpdate,
    _: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    updated = crud.update_project(db, project_id, project)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated


@app.delete("/api/admin/projects/{project_id}", tags=["Admin"])
def admin_delete_project(
    project_id: int,
    _: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # Also delete local image if it's an upload
    project = crud.get_project(db, project_id)
    if project and project.image_url and project.image_url.startswith("/uploads/"):
        file_path = UPLOADS_DIR / Path(project.image_url).name
        if file_path.exists():
            file_path.unlink()
    success = crud.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}


# ────────────────────────────────────────────────────────────────
# Admin: Image Upload
# ────────────────────────────────────────────────────────────────

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
MAX_FILE_SIZE_MB = 10


@app.post("/api/admin/upload-image", tags=["Admin"])
async def upload_image(
    file: UploadFile = File(...),
    _: str = Depends(verify_token),
):
    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not allowed. Use: {', '.join(ALLOWED_EXTENSIONS)}")

    # Read and check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Max size: {MAX_FILE_SIZE_MB}MB")

    # Save with unique name
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOADS_DIR / filename
    with open(file_path, "wb") as f:
        f.write(content)

    return {"url": f"/uploads/{filename}", "filename": filename}


@app.delete("/api/admin/delete-image/{filename}", tags=["Admin"])
def delete_image(filename: str, _: str = Depends(verify_token)):
    # Security: prevent path traversal
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    file_path = UPLOADS_DIR / filename
    if file_path.exists():
        file_path.unlink()
    return {"message": "Image deleted"}


# ────────────────────────────────────────────────────────────────
# Admin: Skills
# ────────────────────────────────────────────────────────────────

@app.post("/api/admin/skills", response_model=schemas.SkillResponse, tags=["Admin"])
def admin_create_skill(
    skill: schemas.SkillCreate,
    _: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return crud.create_skill(db, skill)


@app.put("/api/admin/skills/{skill_id}", response_model=schemas.SkillResponse, tags=["Admin"])
def admin_update_skill(
    skill_id: int,
    skill: schemas.SkillUpdate,
    _: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    updated = crud.update_skill(db, skill_id, skill)
    if not updated:
        raise HTTPException(status_code=404, detail="Skill not found")
    return updated


@app.delete("/api/admin/skills/{skill_id}", tags=["Admin"])
def admin_delete_skill(
    skill_id: int,
    _: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    success = crud.delete_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill deleted"}


# ────────────────────────────────────────────────────────────────
# Health Check
# ────────────────────────────────────────────────────────────────

@app.get("/api/health", tags=["Misc"])
def health():
    return {"status": "ok"}


# ────────────────────────────────────────────────────────────────
# Serve uploads + Frontend (MUST be last — mounts intercept all paths)
# ────────────────────────────────────────────────────────────────

app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/admin", include_in_schema=False)
@app.get("/admin.html", include_in_schema=False)
def serve_admin():
    return FileResponse(str(FRONTEND_DIR / "admin.html"))

@app.get("/projects", include_in_schema=False)
@app.get("/projects.html", include_in_schema=False)
def serve_projects():
    return FileResponse(str(FRONTEND_DIR / "projects.html"))

# Catch-all for other static assets (css, js, images in frontend/)
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
