from typing import List, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.profile import SeniorProfile, YouthProfile
from app.models.user import UserType
import json
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    _model = None
    
    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer('jhgan/ko-sroberta-multitask')
            logger.info("Korean embedding model loaded successfully")
        return cls._model
    
    @classmethod
    def generate_embedding(cls, text: str) -> List[float]:
        if not text or not text.strip():
            return None
        
        model = cls.get_model()
        embedding = model.encode(text)
        return embedding.tolist()
    
    @classmethod
    def calculate_similarity(cls, embedding1: List[float], embedding2: List[float]) -> float:
        if not embedding1 or not embedding2:
            return 0.0
        
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        cosine_similarity = dot_product / (norm1 * norm2)
        return float(cosine_similarity)
    
    @classmethod
    def update_profile_embedding(cls, db: Session, user_id: str, user_type: UserType, profile_text: str):
        embedding = cls.generate_embedding(profile_text)
        
        if user_type == UserType.SENIOR:
            profile = db.query(SeniorProfile).filter(SeniorProfile.user_id == user_id).first()
        else:
            profile = db.query(YouthProfile).filter(YouthProfile.user_id == user_id).first()
        
        if profile:
            profile.profile_text = profile_text
            profile.embedding = embedding
            profile.embedding_updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Updated embedding for {user_type.value} user {user_id}")
            return profile
        
        return None
    
    @classmethod
    async def update_profile_embedding_async(cls, db, user_id: str, user_type: UserType, profile_text: str):
        from sqlalchemy import select
        
        embedding = cls.generate_embedding(profile_text)
        
        if user_type == UserType.SENIOR:
            result = await db.execute(
                select(SeniorProfile).where(SeniorProfile.user_id == user_id)
            )
            profile = result.scalar_one_or_none()
        else:
            result = await db.execute(
                select(YouthProfile).where(YouthProfile.user_id == user_id)
            )
            profile = result.scalar_one_or_none()
        
        if profile:
            profile.profile_text = profile_text
            profile.embedding = embedding
            profile.embedding_updated_at = datetime.utcnow()
            await db.commit()
            logger.info(f"Updated embedding for {user_type.value} user {user_id}")
            return profile
        
        return None
    
    @classmethod
    def find_similar_profiles(
        cls, 
        db: Session, 
        user_id: str, 
        user_type: UserType, 
        limit: int = 10,
        min_similarity: float = 0.5
    ) -> List[Tuple[object, float]]:
        
        if user_type == UserType.SENIOR:
            source_profile = db.query(SeniorProfile).filter(SeniorProfile.user_id == user_id).first()
            target_model = YouthProfile
        else:
            source_profile = db.query(YouthProfile).filter(YouthProfile.user_id == user_id).first()
            target_model = SeniorProfile
        
        if not source_profile or not source_profile.embedding:
            return []
        
        candidates = db.query(target_model).filter(
            target_model.embedding != None
        ).all()
        
        results = []
        for candidate in candidates:
            if candidate.embedding:
                similarity = cls.calculate_similarity(
                    source_profile.embedding, 
                    candidate.embedding
                )
                if similarity >= min_similarity:
                    results.append((candidate, similarity))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    @classmethod
    def batch_update_embeddings(cls, db: Session):
        senior_profiles = db.query(SeniorProfile).filter(
            SeniorProfile.profile_text != None,
            SeniorProfile.embedding == None
        ).all()
        
        for profile in senior_profiles:
            if profile.profile_text:
                embedding = cls.generate_embedding(profile.profile_text)
                profile.embedding = embedding
                profile.embedding_updated_at = datetime.utcnow()
        
        youth_profiles = db.query(YouthProfile).filter(
            YouthProfile.profile_text != None,
            YouthProfile.embedding == None
        ).all()
        
        for profile in youth_profiles:
            if profile.profile_text:
                embedding = cls.generate_embedding(profile.profile_text)
                profile.embedding = embedding
                profile.embedding_updated_at = datetime.utcnow()
        
        db.commit()
        logger.info(f"Batch updated {len(senior_profiles)} senior and {len(youth_profiles)} youth embeddings")