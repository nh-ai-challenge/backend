from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class UserType(str, Enum):
    SENIOR = "senior"
    YOUTH = "youth"


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(SQLEnum(UserType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    senior_profile = relationship("SeniorProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    youth_profile = relationship("YouthProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    youth_vision_profile = relationship("YouthVisionProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")