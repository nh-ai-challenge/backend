from datetime import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, UniqueConstraint, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class MatchStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    senior_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    youth_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    sci_score = Column(Float, nullable=False)
    philosophy_compatibility = Column(Float, nullable=False)
    business_compatibility = Column(Float, nullable=False)
    mentorship_compatibility = Column(Float, nullable=False)
    finance_compatibility = Column(Float, nullable=False)
    
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING, nullable=False)
    
    senior_persona_type = Column(String(50))
    youth_persona_type = Column(String(50))
    
    location_distance_km = Column(Float)
    crop_match = Column(Boolean, default=False)
    
    ai_recommendation = Column(String(50))
    compatibility_details = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    senior = relationship("User", foreign_keys=[senior_id], back_populates="senior_matches")
    youth = relationship("User", foreign_keys=[youth_id], back_populates="youth_matches")
    
    __table_args__ = (
        UniqueConstraint('senior_id', 'youth_id', name='unique_senior_youth_match'),
    )


class MatchRequest(Base):
    __tablename__ = "match_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    match_id = Column(UUID(as_uuid=True), ForeignKey("matches.id", ondelete="CASCADE"))
    
    message = Column(String(500))
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True))
    
    requester = relationship("User", foreign_keys=[requester_id])
    target = relationship("User", foreign_keys=[target_id])
    match = relationship("Match")


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