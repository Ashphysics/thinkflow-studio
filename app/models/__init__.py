"""
Database Models Package for ThinkFlow Studio.

Contains SQLAlchemy ORM model declarations mapping database tables for session management,
audit trails, and memory entries.

TODOs:
    - [ ] Setup Alembic configuration hooks for database migration automations.
    - [ ] Create SQLite JSON custom data loaders for backward compatibility.
"""

from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    SQLAlchemy Declarative Base class.
    """
    pass


class SessionModel(Base):
    """
    Model representing a planning session instance.
    """
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="initialized")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class AgentRunModel(Base):
    """
    Model logging audit records of a specific agent run.
    """
    __tablename__ = "agent_runs"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(index=True, nullable=False)
    agent_name: Mapped[str] = mapped_column(nullable=False)
    model_name: Mapped[str] = mapped_column(nullable=False)
    input_data: Mapped[str] = mapped_column(nullable=False)  # JSON String
    output_data: Mapped[str] = mapped_column(nullable=False) # JSON String
    executed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
