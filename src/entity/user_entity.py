import os
from typing import Optional
from datetime import datetime

try:
    from redis_om import HashModel, Field
except Exception:
    HashModel = object
    Field = lambda *a, **k: None


from src.service.redis_service import RedisService

def _get_redis_connection():
    return RedisService.get_redis_om_connection()


from sqlalchemy import Column, String, Boolean, DateTime, Integer, func
from src.config.db_dev import Base

class UserEntity(Base):
    __tablename__ = "users"

    username = Column(String(191), primary_key=True, index=True, nullable=False)
    email = Column(String(191), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    role = Column(String(32), nullable=False, default="user")
    role_level = Column(Integer, nullable=False, default=10)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

