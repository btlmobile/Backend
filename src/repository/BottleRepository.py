from typing import Optional
from sqlalchemy.orm import Session
from src.entity.bottle_entity import BottleEntity
import uuid


class BottleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, bottle_id: str) -> Optional[BottleEntity]:
        return self.db.query(BottleEntity).filter(BottleEntity.id == bottle_id).first()

    def create_bottle(
        self,
        sender_username: str,
        message: str,
    ) -> BottleEntity:
        bottle_id = str(uuid.uuid4())
        bottle = BottleEntity(
            id=bottle_id,
            sender_username=sender_username,
            message=message,
        )
        self.db.add(bottle)
        self.db.commit()
        self.db.refresh(bottle)
        return bottle
