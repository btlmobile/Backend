from typing import Optional
from sqlalchemy.orm import Session
from src.entity.user_entity import UserEntity
from src.constant.role import Role, get_role_level


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[UserEntity]:
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        return self.db.query(UserEntity).filter(UserEntity.email == email).first()

    def create_user(
        self,
        username: str,
        email: str,
        full_name: Optional[str],
        hashed_password: str,
        role: Role = Role.USER,
    ) -> UserEntity:
        user = UserEntity(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True,
            role=role.value,
            role_level=get_role_level(role.value),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
