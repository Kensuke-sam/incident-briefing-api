from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models


class IncidentReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, record: models.IncidentReport) -> models.IncidentReport:
        self.db.add(record)
        return record

    def get_by_id(self, record_id: str) -> models.IncidentReport | None:
        statement = select(models.IncidentReport).where(models.IncidentReport.id == record_id)
        return self.db.scalar(statement)


class IncidentBriefingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, record: models.IncidentBriefing) -> models.IncidentBriefing:
        self.db.add(record)
        return record

    def get_by_incident_report_id(self, record_id: str) -> models.IncidentBriefing | None:
        statement = select(models.IncidentBriefing).where(
            models.IncidentBriefing.incident_report_id == record_id,
        )
        return self.db.scalar(statement)
