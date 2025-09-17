from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class SeniorProfileV2(Base):
    __tablename__ = "senior_profiles_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    basic_info = Column(JSON)
    successor_pref = Column(JSON)
    conditions = Column(JSON)
    vision = Column(JSON)
    
    philosophy_score = Column(Float)
    experience_required = Column(Integer)
    price_min = Column(Integer)
    price_max = Column(Integer)
    timeline_months = Column(Integer)
    mentoring_willingness = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="senior_profile_v2")


class YouthProfileV2(Base):
    __tablename__ = "youth_profiles_v2"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    basic_info = Column(JSON)
    vision_info = Column(JSON)
    partnership = Column(JSON)
    finance = Column(JSON)
    
    philosophy_score = Column(Float)
    experience_level = Column(Integer)
    capital_min = Column(Integer)
    capital_max = Column(Integer)
    timeline_months = Column(Integer)
    mentorship_need_level = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="youth_profile_v2")


class YouthVisionProfile(Base):
    __tablename__ = "youth_vision_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    goal = Column(String(50))
    experience = Column(Text)
    skills = Column(JSON)
    vision = Column(Text)
    conditions = Column(JSON)
    profile_photos = Column(JSON)
    greeting = Column(Text)
    
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="youth_vision_profile")