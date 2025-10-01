from datetime import datetime, timedelta, UTC
import jwt
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.helper.settings_helper import load_settings
from sqlalchemy.orm import Session
from src.helper.db_session import get_db
from src.repository.UserRepository import UserRepository

settings = load_settings()
jwt_cfg = settings.get("jwt", {})
SECRET = jwt_cfg.get("secret", "change-me-to-a-secure-secret")
ALGORITHM = jwt_cfg.get("algorithm", "HS256")
EXPIRE_MINUTES = int(jwt_cfg.get("expire_minutes", 60))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None, extra_claims: Optional[Dict[str, Any]] = None) -> str:
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
    if extra_claims:
        to_encode.update(extra_claims)
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")
    username = payload["sub"]
    repo = UserRepository(db)
    user = repo.get_by_username(username)
    if not user or getattr(user, "is_active", False) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="inactive_or_not_found")
    return user
