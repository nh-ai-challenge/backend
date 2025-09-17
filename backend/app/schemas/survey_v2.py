from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class SeniorSurveySection(BaseModel):
    basic_info: Dict[str, Any] = Field(..., description="농장 기본 정보")
    successor_pref: Dict[str, Any] = Field(..., description="승계자 선호도")
    conditions: Dict[str, Any] = Field(..., description="승계 조건")
    vision: Dict[str, Any] = Field(..., description="농장 비전")


class YouthSurveySection(BaseModel):
    basic_info: Dict[str, Any] = Field(..., description="기본 정보")
    vision_info: Dict[str, Any] = Field(..., description="비전 정보")
    partnership: Dict[str, Any] = Field(..., description="파트너십")
    finance: Dict[str, Any] = Field(..., description="재정 정보")


class VisionProfileRequest(BaseModel):
    goal: str = Field(..., max_length=50, description="목표")
    experience: str = Field(..., description="경험")
    skills: List[str] = Field(..., description="보유 기술")
    vision: str = Field(..., description="비전")
    conditions: Dict[str, Any] = Field(..., description="희망 조건")
    profile_photos: Optional[List[str]] = Field(None, description="프로필 사진 URL")
    greeting: str = Field(..., description="인사말")


class ProfileResponseBase(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class SeniorProfileResponse(ProfileResponseBase):
    basic_info: Dict[str, Any]
    successor_pref: Dict[str, Any]
    conditions: Dict[str, Any]
    vision: Dict[str, Any]
    philosophy_score: Optional[float]
    experience_required: Optional[int]
    price_min: Optional[int]
    price_max: Optional[int]
    timeline_months: Optional[int]
    mentoring_willingness: Optional[bool]
    
    class Config:
        from_attributes = True


class YouthProfileResponse(ProfileResponseBase):
    basic_info: Dict[str, Any]
    vision_info: Dict[str, Any]
    partnership: Dict[str, Any]
    finance: Dict[str, Any]
    philosophy_score: Optional[float]
    experience_level: Optional[int]
    capital_min: Optional[int]
    capital_max: Optional[int]
    timeline_months: Optional[int]
    mentorship_need_level: Optional[int]
    
    class Config:
        from_attributes = True


class VisionProfileResponse(ProfileResponseBase):
    goal: Optional[str]
    experience: Optional[str]
    skills: Optional[List[str]]
    vision: Optional[str]
    conditions: Optional[Dict[str, Any]]
    profile_photos: Optional[List[str]]
    greeting: Optional[str]
    completed: bool
    
    class Config:
        from_attributes = True


class SurveySubmissionResult(BaseModel):
    profile_id: UUID
    philosophy_score: float
    experience_score: Optional[float] = None
    financial_score: Optional[float] = None
    timeline_score: Optional[float] = None
    mentorship_score: Optional[float] = None
    message: str