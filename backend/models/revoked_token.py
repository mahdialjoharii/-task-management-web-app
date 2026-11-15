from sqlalchemy import Column, String, DateTime
from database.database import Base


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    jti = Column(String(36), primary_key=True)

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )