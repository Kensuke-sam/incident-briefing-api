from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.errors import NotFoundError, PersistenceError
from app.repositories import IncidentBriefingRepository, IncidentReportRepository
from app.services.ai import IncidentAiService


class IncidentService:
    def __init__(self, db: Session, ai_service: IncidentAiService) -> None:
        self.db = db
        self.ai_service = ai_service
        self.entities = IncidentReportRepository(db)
        self.analyses = IncidentBriefingRepository(db)

    def create_incident(self, payload: schemas.IncidentCreate) -> schemas.IncidentResponse:
        record = models.IncidentReport(
            service_name=payload.service_name,
            alert_summary=payload.alert_summary,
            timeline=payload.timeline,
        )
        try:
            self.entities.create(record)
            self.db.commit()
            self.db.refresh(record)
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise PersistenceError("Failed to save 障害レポート.") from exc
        return schemas.IncidentResponse.model_validate(record)

    def get_incident(self, record_id: str) -> schemas.IncidentResponse:
        record = self.entities.get_by_id(record_id)
        if record is None:
            raise NotFoundError("障害レポート not found.")
        return schemas.IncidentResponse.model_validate(record)

    def brief_incident(self, record_id: str) -> schemas.IncidentBriefingResponse:
        record = self.entities.get_by_id(record_id)
        if record is None:
            raise NotFoundError("障害レポート not found.")

        draft = self.ai_service.generate(record)
        existing = self.analyses.get_by_incident_report_id(record_id)
        if existing is None:
            existing = models.IncidentBriefing(
                incident_report_id=record_id,
                **draft.model_dump(),
            )
            self.analyses.save(existing)
        else:
            existing.probable_cause = draft.probable_cause
            existing.severity = draft.severity
            existing.next_actions = draft.next_actions
            existing.customer_impact = draft.customer_impact

        try:
            self.db.commit()
            self.db.refresh(existing)
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise PersistenceError("Failed to save ブリーフィング.") from exc

        return schemas.IncidentBriefingResponse.model_validate(existing)

    def get_briefing(self, record_id: str) -> schemas.IncidentBriefingResponse:
        record = self.entities.get_by_id(record_id)
        if record is None:
            raise NotFoundError("障害レポート not found.")

        analysis = self.analyses.get_by_incident_report_id(record_id)
        if analysis is None:
            raise NotFoundError("ブリーフィング not found.")
        return schemas.IncidentBriefingResponse.model_validate(analysis)
