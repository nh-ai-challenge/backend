from datetime import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class MatchingScore(Base):
    __tablename__ = "matching_scores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    senior_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    youth_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    sci_total_score = Column(Float, nullable=False)
    
    philosophy_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    financial_score = Column(Float, nullable=False)
    timeline_score = Column(Float, nullable=False)
    mentorship_score = Column(Float, nullable=False)
    
    location_bonus = Column(Float, default=0)
    crop_bonus = Column(Float, default=0)
    
    ai_recommendation = Column(String(50))
    ai_insights = Column(Text)
    
    mutual_interest = Column(String(20), default="none")
    
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    senior = relationship("User", foreign_keys=[senior_id], backref="matches_as_senior")
    youth = relationship("User", foreign_keys=[youth_id], backref="matches_as_youth")
    
    __table_args__ = (
        UniqueConstraint('senior_id', 'youth_id', name='_senior_youth_uc'),
    )