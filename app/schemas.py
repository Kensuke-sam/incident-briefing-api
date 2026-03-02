from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class IncidentCreate(BaseModel):
    service_name: str = Field(min_length=3, max_length=80, description="Affected service name")
    alert_summary: str = Field(min_length=10, max_length=160, description="Alert summary")
    timeline: str = Field(min_length=30, max_length=6000, description="Incident timeline")


class IncidentResponse(IncidentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


class IncidentBriefingDraft(BaseModel):
    probable_cause: str = Field(min_length=10, max_length=400, description="Probable cause")
    severity: str = Field(min_length=3, max_length=16, description="Severity level")
    next_actions: list[str] = Field(min_length=1, description="Next actions")
    customer_impact: str = Field(min_length=10, max_length=400, description="Customer impact")


class IncidentBriefingResponse(IncidentBriefingDraft):
    model_config = ConfigDict(from_attributes=True)

    id: str
    incident_report_id: str
    created_at: datetime
