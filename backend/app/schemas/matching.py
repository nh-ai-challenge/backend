from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class MatchStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class MatchResponse(BaseModel):
    match_id: UUID
    partner_id: UUID
    partner_type: str
    sci_score: float = Field(..., ge=0, le=100)
    philosophy_compatibility: float
    business_compatibility: float
    mentorship_compatibility: float
    finance_compatibility: float
    status: MatchStatusEnum
    ai_recommendation: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class MatchDetailResponse(BaseModel):
    match_id: UUID
    partner_id: UUID
    partner_name: str
    partner_type: str
    sci_score: float = Field(..., ge=0, le=100)
    philosophy_compatibility: float
    business_compatibility: float
    mentorship_compatibility: float
    finance_compatibility: float
    senior_persona_type: Optional[str] = None
    youth_persona_type: Optional[str] = None
    location_distance_km: Optional[float] = None
    crop_match: bool = False
    compatibility_details: Optional[str] = None
    ai_recommendation: Optional[str] = None
    status: MatchStatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MatchCalculateRequest(BaseModel):
    senior_id: UUID
    youth_id: UUID


class MatchCalculateResponse(BaseModel):
    match_id: UUID
    senior_id: UUID
    youth_id: UUID
    sci_score: float = Field(..., ge=0, le=100)
    philosophy_compatibility: float
    business_compatibility: float
    mentorship_compatibility: float
    finance_compatibility: float
    ai_recommendation: Optional[str] = None
    compatibility_details: Optional[str] = None
    
    class Config:
        from_attributes = True


class MatchStatusUpdate(BaseModel):
    status: MatchStatusEnum


class MatchRequestCreate(BaseModel):
    target_id: UUID
    message: Optional[str] = Field(None, max_length=500)


class MatchRequestResponse(BaseModel):
    request_id: UUID
    requester_id: UUID
    target_id: UUID
    match_id: Optional[UUID] = None
    message: Optional[str] = None
    status: MatchStatusEnum
    created_at: datetime
    responded_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True