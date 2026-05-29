from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API is running"}


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Request Models
class LoginRequest(BaseModel):
    email: str
    password: str


class FormRequest(BaseModel):
    name: str
    age: int
    salary: float
    department: str


# LOGIN API
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    try:
        user = db.query(models.User).filter(
            models.User.email == data.email,
            models.User.password == data.password
        ).first()

        if user:
            return {
                "success": True,
                "message": "Login successful"
            }

        return {
            "success": False,
            "message": "Invalid credentials"
        }

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# SUBMIT FORM API
@app.post("/submit-form")
def submit_form(data: FormRequest, db: Session = Depends(get_db)):

    try:
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

    except Exception as e:
        print("FORM ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# CHART DATA API
@app.get("/chart-data")
def chart_data(db: Session = Depends(get_db)):

    try:
        data = db.query(models.FormData).all()

        result = []

        for item in data:
            result.append({
                "name": item.name,
                "salary": float(item.salary)
            })

        return result

    except Exception as e:
        print("CHART ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))