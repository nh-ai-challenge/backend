from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class SurveyAnswer(BaseModel):
    question_id: str
    question_text: str
    answer: str
    score: Optional[int] = None
    dimension: Optional[str] = None


class SurveySubmit(BaseModel):
    answers: List[SurveyAnswer]


class SurveyResponse(BaseModel):
    id: UUID
    user_id: UUID
    question_id: str
    question_text: str
    answer: str
    score: Optional[int]
    dimension: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PersonaResponse(BaseModel):
    id: UUID
    user_id: UUID
    persona_type: str
    persona_name: str
    persona_description: str
    philosophy_score: float
    business_score: float
    mentorship_score: float
    finance_score: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: str
    section: int
    text: str
    type: str
    options: Optional[List[str]] = None
    dimension: Optional[str] = None
    order: int