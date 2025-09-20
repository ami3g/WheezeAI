
from backend.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate, UserRead
from backend.services.user import create_user, get_user, get_user_by_email
from backend.models.user import User
from backend.db import SessionLocal
from backend.utils.auth import create_access_token
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=UserRead)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.get("/users/me")
def read_current_user(request: Request):
    print(f"DEBUG: /users/me endpoint called successfully!")
    
    # Manually extract Authorization header
    auth_header = request.headers.get("Authorization")
    print(f"DEBUG: Authorization header: {auth_header}")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = auth_header.split(" ")[1]
    print(f"DEBUG: Extracted token: {token[:20]}...")
    
    # Decode token
    from backend.utils.auth import decode_access_token
    payload = decode_access_token(token)
    print(f"DEBUG: Decoded payload: {payload}")
    
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Get user
    user_id = int(payload["sub"])
    print(f"DEBUG: Looking for user_id: {user_id}")
    
    from backend.db import SessionLocal
    from backend.models.user import User
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    print(f"DEBUG: Found user: {user}")
    print(f"DEBUG: Returning user data: id={user.id}, name={user.name}, email={user.email}, role={user.role}, is_active={user.is_active}")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    print(f"DEBUG: read_user endpoint called for user_id: {user_id}")
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
