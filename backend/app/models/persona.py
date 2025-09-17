from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class PersonaType:
    ARTISAN_SUCCESSOR = "artisan_successor"
    EXPERIENCED_ENTREPRENEUR = "experienced_entrepreneur"
    DATA_DRIVEN_ARTISAN = "data_driven_artisan"
    INNOVATIVE_MANAGER = "innovative_manager"


class Persona(Base):
    __tablename__ = "personas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    persona_type = Column(String(50), nullable=False)
    philosophy_score = Column(Float, nullable=False)
    business_score = Column(Float, nullable=False)
    mentorship_score = Column(Float, nullable=False)
    finance_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="persona")