from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import secrets
import string

from datetime import datetime

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
    
class CreateUserRequest(BaseModel):
    full_name: str
    email: str
    role_id: int

# Generate Random Password
def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(secrets.choice(chars) for _ in range(length))


# LOGIN API
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    try:
        user = db.query(models.User).filter(
            models.User.email == data.email,
            models.User.password == data.password
        ).first()

        if user:
            user.status_id = 2 
            user.last_login = datetime.utcnow()
            db.commit()
            db.refresh(user)

            role = db.query(models.Roles).filter(
                models.Roles.id == user.role_id
            ).first()

            status = db.query(models.UserStatus).filter(
                models.UserStatus.id == user.status_id
            ).first()

            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role_id": user.role_id,
                    "role_name": role.role_name if role else None,
                    "status_id": user.status_id,
                    "status_name": status.status_name if status else None,
                    "last_login": user.last_login
                }
            }

        return {
            "success": False,
            "message": "Invalid credentials"
        }

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).all()

        result = []

        for user in users:
            role = db.query(models.Roles).filter(
                models.Roles.id == user.role_id
            ).first()

            status = db.query(models.UserStatus).filter(
                models.UserStatus.id == user.status_id
            ).first()

            result.append({
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role_id": user.role_id,
                "role_name": role.role_name if role else None,
                "status_id": user.status_id,
                "status_name": status.status_name if status else None,
                "created_on": user.created_at,
                "last_login": user.last_login
            })

        return {
            "success": True,
            "count": len(result),
            "users": result
        }

    except Exception as e:
        print("GET USERS ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Generate User API
@app.post("/users")
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    random_password = generate_password()

    new_user = models.User(
        full_name=data.full_name,
        email=data.email,
        password=random_password,
        role_id=data.role_id,
        status_id=1,
        created_at=datetime.utcnow(),
        last_login=None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "User created successfully",
        "user_id": new_user.id,
        "generated_password": random_password
    }

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