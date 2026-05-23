"""
seed.py — Populate the database with the original portfolio data.
Run once: python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
import models
import crud
from schemas import ProjectCreate, SkillCreate

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ── Clear existing data ──────────────────────────────────────────
db.query(models.Project).delete()
db.query(models.Skill).delete()
db.commit()

# ── Projects ─────────────────────────────────────────────────────
projects = [
    ProjectCreate(
        title="FitVision",
        description="AI-powered computer vision project utilizing machine learning for real-time form analysis and biomechanical tracking. Built with focus on low-latency inference.",
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuBAhg4E9zQK5zV2habfaGi1GRCqMP8Hx2XwH3caulKKRBUlCb3nfLdmPRqSGqBxx7nbE22poPzEV3rIoZlkKM5gt8slKq-ZPaKzq_L21ydzHZWSdu3V3nGYSFHRCfEg3j35LHBJ6jN9x5f6-JECXl2lfGTVmLuGR6OOG4czoTQJ4PoK7m11oHy0l8Y-F3DZAnX7yKCEJf4GAPo_JZBGbu02klfwYk0ivzZYzdiLkX9iiOgoLkFNKuRZulhtCQOT1U2HYrN2j2ES_gWD",
        demo_url="#",
        github_url="#",
        tags=["MediaPipe", "Python", "React"],
        is_flagship=True,
        order=1,
    ),
    ProjectCreate(
        title="AlgoLab",
        description="Interactive algorithmic visualization platform designed to clarify complex data structures and execution flows.",
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuBSR7gr55BQnyzU_Hl1GXaw3IwKgvlE33uLdpIpqp_ykrMn8uUdTNIIk-hp0zvEreb6mBbJAsiMTXb7ysE-G4ojvkGPCHgtZsOXcIQ7TTFT4Rs7dpgBfzNOOkJDhV1nURdObgvvTeD5w_a41sm-OZdDfQWVPBocIL4AMo24g5_h17HNQM58PXYvqzKJ-sznw_4QilYQGLlriLjbiDU--e0BWiDC1pt7Se_TCyaZCF7aSCHjpFdJaUtEYNEwylH2ntDreL4Y7L3dZS5_",
        demo_url="#",
        github_url="#",
        tags=["React", "Tailwind"],
        is_flagship=False,
        order=2,
    ),
    ProjectCreate(
        title="Deadline Tracker",
        description="High-performance real-time data scraping dashboard aggregating critical timelines across distributed sources. Engineered for high concurrency.",
        image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCG5jXTAhk-rm8Id9UwEqoDdTBwudV-moI-5zNXXcrZtkgzv3phbTbkleGh1NSQHZUy3jXtBGEh-jxANHJGjnAHtgyE6pQm_ZFokCh4qMrCgOuLEO01w8ko4OgLVTxsVBfeDktz8hXOudfNt2NjlNanmSwgDtbfOz5_nIfcHm0nKCIhbdV-To5aMkXF4NKLfSfMYcAxEgAcws-Y4IGURIcGpIwScxVG6R8c6IEJiggF4CzMszc8gLFjeugC-OfsuDH0_Vyf0s0PURP5",
        demo_url="#",
        github_url="#",
        tags=["FastAPI", "Python", "PostgreSQL"],
        is_flagship=False,
        order=3,
    ),
]

for p in projects:
    crud.create_project(db, p)
    print(f"  [OK] Project: {p.title}")

# ── Skills ────────────────────────────────────────────────────────
skills = [
    # Frontend
    SkillCreate(name="React / Next.js", category="Frontend", order=1),
    SkillCreate(name="Tailwind CSS", category="Frontend", order=2),
    SkillCreate(name="TypeScript", category="Frontend", order=3),
    # Backend
    SkillCreate(name="Python / FastAPI", category="Backend", order=1),
    SkillCreate(name="Node.js / Express", category="Backend", order=2),
    SkillCreate(name="PostgreSQL / Redis", category="Backend", order=3),
    # Cloud
    SkillCreate(name="Docker / K8s", category="Cloud", order=1),
    SkillCreate(name="CI/CD Pipelines", category="Cloud", order=2),
    SkillCreate(name="AWS / Nginx", category="Cloud", order=3),
]

for s in skills:
    crud.create_skill(db, s)
    print(f"  [OK] Skill: {s.name} ({s.category})")

db.close()
print("\nSeed complete!")
