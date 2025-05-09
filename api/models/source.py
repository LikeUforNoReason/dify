import json
import uuid

from sqlalchemy import func

from models.base import Base

from .engine import db
from .types import AdjustedJSON, PostgresJSONIndex, StringUUID


class DataSourceOauthBinding(db.Model):  # type: ignore[name-defined]
    __tablename__ = "data_source_oauth_bindings"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="source_binding_pkey"),
        db.Index("source_binding_tenant_id_idx", "tenant_id"),
        PostgresJSONIndex("source_info_idx", "source_info", postgresql_using="gin"),
    )

    id = db.Column(StringUUID, default=lambda: uuid.uuid4())
    tenant_id = db.Column(StringUUID, nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    provider = db.Column(db.String(255), nullable=False)
    source_info = db.Column(AdjustedJSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    disabled = db.Column(db.Boolean, nullable=True, default=False)


class DataSourceApiKeyAuthBinding(Base):
    __tablename__ = "data_source_api_key_auth_bindings"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="data_source_api_key_auth_binding_pkey"),
        db.Index("data_source_api_key_auth_binding_tenant_id_idx", "tenant_id"),
        db.Index("data_source_api_key_auth_binding_provider_idx", "provider"),
    )

    id = db.Column(StringUUID, default=lambda: uuid.uuid4())
    tenant_id = db.Column(StringUUID, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    provider = db.Column(db.String(255), nullable=False)
    credentials = db.Column(db.Text, nullable=True)  # JSON
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    disabled = db.Column(db.Boolean, nullable=True, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "category": self.category,
            "provider": self.provider,
            "credentials": json.loads(self.credentials),
            "created_at": self.created_at.timestamp(),
            "updated_at": self.updated_at.timestamp(),
            "disabled": self.disabled,
        }
