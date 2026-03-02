from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def generate_id() -> str:
    return str(uuid4())


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class IncidentReport(Base, TimestampMixin):
    __tablename__ = "incident_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_id)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    alert_summary: Mapped[str] = mapped_column(String(255), nullable=False)
    timeline: Mapped[str] = mapped_column(Text, nullable=False)


class IncidentBriefing(Base, TimestampMixin):
    __tablename__ = "incident_briefings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_id)
    incident_report_id: Mapped[str] = mapped_column(
        ForeignKey("incident_reports.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    probable_cause: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(255), nullable=False)
    next_actions: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    customer_impact: Mapped[str] = mapped_column(Text, nullable=False)
