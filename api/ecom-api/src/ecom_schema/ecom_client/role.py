"""SQLAlchemy ORM for ecom_client role domain."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy import ARRAY, Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

SCHEMA = "ecom_client"

class Role(Base):
    """Role definition for user permissions."""

    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(1024))
    permissions: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))