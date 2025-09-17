from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Survey(Base):
    __tablename__ = "surveys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String(20), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    score = Column(Integer)
    dimension = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="surveys")


class SurveyQuestion(Base):
    __tablename__ = "survey_questions"
    
    id = Column(String(20), primary_key=True)
    user_type = Column(String(20), nullable=False)
    section = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    dimension = Column(String(50))
    options = Column(Text)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)