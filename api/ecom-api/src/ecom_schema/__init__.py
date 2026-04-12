from ._meta import config, logger
import sqlalchemy as sa
from datetime import datetime, UTC
from typing import Optional, Type

from sqlalchemy import create_engine, MetaData, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from fluvius.data import DomainSchema, SqlaDriver


# --- Connector and Base Schema ---
class EcomConnector(SqlaDriver):
    __db_dsn__ = config.DB_DSN
    __schema__ = config.DB_SCHEMA


def create_base_model(schema_name: str, driver_cls: Optional[Type[EcomConnector]] = None):
    """
    Create a SQLAlchemy declarative base with a specific schema name.
    All models will inherit audit fields (_created, _updated).

    Args:
        schema_name: The PostgreSQL schema name to use for all tables

    Returns:
        Declarative base class configured with the specified schema and audit fields
    """

    # Create a new base that includes the audit mixin
    driver_cls = driver_cls or EcomConnector

    class EcomBaseSchema(EcomConnector.__data_schema_base__, DomainSchema):
        __abstract__ = True
        __table_args__ = {"schema": schema_name}
        _realm = sa.Column(sa.String(255), nullable=True)

    return EcomBaseSchema


def create_view_model(schema_name: str, driver_cls: Optional[Type[EcomConnector]] = None):
    """
    Create a SQLAlchemy declarative base for database views without audit columns.
    """
    driver_cls = driver_cls or EcomConnector

    class EcomViewSchema(EcomConnector.__data_schema_base__):
        __abstract__ = True
        __table_args__ = {"schema": schema_name}

    return EcomViewSchema

EcomConnector = EcomConnector

__all__ = [
    "EcomConnector",
    "create_base_model",
    "create_view_model",
    "config",
    "logger",
]

from . import _schema as _schema_module
