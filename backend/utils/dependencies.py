from fastapi import Depends, HTTPException, Header
from jose import JWTError, jwt

from backend.utils.auth import SECRET_KEY, ALGORITHM, decode_access_token
from backend.db import SessionLocal
from backend.models.user import User


def get_current_user(authorization: str = Header(None)):
    print(f"DEBUG: Authorization header: {authorization}")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not authorization or not authorization.startswith("Bearer "):
        print("DEBUG: Missing or invalid Authorization header")
        raise credentials_exception
    
    token = authorization.split(" ")[1]
    print(f"DEBUG: Extracted token: {token[:20]}...")
    
    payload = decode_access_token(token)
    print(f"DEBUG: Decoded payload: {payload}")
    if payload is None or "sub" not in payload:
        print("DEBUG: Invalid token or missing 'sub' claim")
        raise credentials_exception
    user_id = int(payload["sub"])
    print(f"DEBUG: Looking for user_id: {user_id}")
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None:
        print(f"DEBUG: No user found for user_id {user_id}")
        raise credentials_exception
    print(f"DEBUG: Found user: {user}")
    print(f"DEBUG: User attributes: id={user.id}, name={user.name}, email={user.email}, role={user.role}, is_active={user.is_active} (type: {type(user.is_active)})")
    return user
