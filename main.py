from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Request Models
# -------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


class FormRequest(BaseModel):
    name: str
    age: int
    salary: float
    department: str


# -------------------------
# Login API
# -------------------------

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    try:
        user = db.query(models.User).filter(
            models.User.email == data.email
        ).first()

        if not user:
            return {"success": False, "message": "User not found"}

        # TEMP FIX (until you add hashing)
        if user.hashed_password != data.password:
            return {"success": False, "message": "Invalid credentials"}

        return {
            "success": True,
            "message": "Login successful"
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

# @app.post("/login")
# def login(data: LoginRequest):

#     db: Session = SessionLocal()

#     user = db.query(models.User).filter(
#         models.User.email == data.email,
#         models.User.hashed_password == data.password
#     ).first()

#     if user:
#         return {
#             "success": True,
#             "message": "Login successful"
#         }

#     return {
#         "success": False,
#         "message": "Invalid credentials"
#     }


# -------------------------
# Submit Form API
# -------------------------

@app.post("/submit-form")
def submit_form(data: FormRequest):

    db: Session = SessionLocal()

    form = models.FormData(
        name=data.name,
        age=data.age,
        salary=data.salary,
        department=data.department
    )

    db.add(form)
    db.commit()

    return {
        "success": True,
        "message": "Data saved"
    }


# -------------------------
# Chart Data API
# -------------------------

@app.get("/chart-data")
def chart_data():

    db: Session = SessionLocal()

    data = db.query(models.FormData).all()

    result = []

    for item in data:
        result.append({
            "name": item.name,
            "salary": float(item.salary)
        })

    return result