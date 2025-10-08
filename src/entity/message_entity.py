from sqlalchemy import Column, String, ForeignKey
from src.config.db_dev import Base


class MessageEntity(Base):
    __tablename__ = "messages"

    id = Column(String(191), primary_key=True, index=True, nullable=False)
    reply_from_id = Column(String(191), ForeignKey("messages.id"), nullable=True)
    bottle_id = Column(String(191), ForeignKey("bottles.id"), nullable=True)
