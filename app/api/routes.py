from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas
from app.core.security import verify_internal_api_key
from app.db import get_db
from app.services.ai import IncidentAiService
from app.services.domain import IncidentService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> IncidentService:
    return IncidentService(db=db, ai_service=IncidentAiService())


@router.get("/healthz", response_model=schemas.HealthResponse)
def healthz() -> schemas.HealthResponse:
    return schemas.HealthResponse()


@router.post(
    "/incidents",
    response_model=schemas.IncidentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_internal_api_key)],
)
def create_record(
    payload: schemas.IncidentCreate,
    service: IncidentService = Depends(get_service),
) -> schemas.IncidentResponse:
    return service.create_incident(payload)


@router.get(
    "/incidents/{record_id}",
    response_model=schemas.IncidentResponse,
    dependencies=[Depends(verify_internal_api_key)],
)
def get_record(
    record_id: str,
    service: IncidentService = Depends(get_service),
) -> schemas.IncidentResponse:
    return service.get_incident(record_id)


@router.post(
    "/incidents/{record_id}/brief",
    response_model=schemas.IncidentBriefingResponse,
    dependencies=[Depends(verify_internal_api_key)],
)
def analyze_record(
    record_id: str,
    service: IncidentService = Depends(get_service),
) -> schemas.IncidentBriefingResponse:
    return service.brief_incident(record_id)


@router.get(
    "/incidents/{record_id}/briefing",
    response_model=schemas.IncidentBriefingResponse,
    dependencies=[Depends(verify_internal_api_key)],
)
def get_analysis(
    record_id: str,
    service: IncidentService = Depends(get_service),
) -> schemas.IncidentBriefingResponse:
    return service.get_briefing(record_id)
