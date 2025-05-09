import uuid

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

from .engine import db
from .model import Message
from .types import StringUUID


class SavedMessage(Base):
    __tablename__ = "saved_messages"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="saved_message_pkey"),
        db.Index("saved_message_message_idx", "app_id", "message_id", "created_by_role", "created_by"),
    )

    id = db.Column(StringUUID, default=lambda: uuid.uuid4())
    app_id = db.Column(StringUUID, nullable=False)
    message_id = db.Column(StringUUID, nullable=False)
    created_by_role = db.Column(db.String(255), nullable=False, default="end_user")
    created_by = db.Column(StringUUID, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())

    @property
    def message(self):
        return db.session.query(Message).filter(Message.id == self.message_id).first()


class PinnedConversation(Base):
    __tablename__ = "pinned_conversations"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pinned_conversation_pkey"),
        db.Index("pinned_conversation_conversation_idx", "app_id", "conversation_id", "created_by_role", "created_by"),
    )

    id = db.Column(StringUUID, default=lambda: uuid.uuid4())
    app_id = db.Column(StringUUID, nullable=False)
    conversation_id: Mapped[str] = mapped_column(StringUUID)
    created_by_role = db.Column(db.String(255), nullable=False, default="end_user")
    created_by = db.Column(StringUUID, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
