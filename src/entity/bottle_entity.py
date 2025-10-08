from sqlalchemy import Column, String, ForeignKey, Text
from src.config.db_dev import Base


class BottleEntity(Base):
    __tablename__ = "bottles"

    id = Column(String(191), primary_key=True, index=True, nullable=False)
    sender_username = Column(String(191), ForeignKey("users.username"), nullable=True)
    message = Column(Text, nullable=False)
