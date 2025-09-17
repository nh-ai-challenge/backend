from typing import Dict, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile_v2 import SeniorProfileV2, YouthProfileV2, YouthVisionProfile
from app.models.user import User
from uuid import UUID


class SurveyV2Service:
    
    @staticmethod
    def calculate_scores_from_senior_survey(data: Dict[str, Any]) -> Dict[str, Any]:
        scores = {}
        
        basic_info = data.get("basic_info", {})
        if "operation_years" in basic_info:
            scores["experience_required"] = max(1, min(basic_info["operation_years"] // 5, 5))
        
        successor_pref = data.get("successor_pref", {})
        if "philosophy" in successor_pref:
            philosophy_map = {
                "tradition": 90,
                "business": 10,
                "mixed": 50
            }
            scores["philosophy_score"] = philosophy_map.get(successor_pref["philosophy"], 50)
        
        if "mentoring" in successor_pref:
            scores["mentoring_willingness"] = successor_pref["mentoring"] in ["active", "moderate"]
        
        conditions = data.get("conditions", {})
        if "price" in conditions:
            scores["price_min"] = conditions["price"].get("min", 0)
            scores["price_max"] = conditions["price"].get("max", 0)
        
        if "timeline" in conditions:
            timeline_map = {
                "immediate": 3,
                "6months": 6,
                "1year": 12,
                "1-3years": 24,
                "3years+": 36
            }
            scores["timeline_months"] = timeline_map.get(conditions["timeline"], 12)
        
        return scores
    
    @staticmethod
    def calculate_scores_from_youth_survey(data: Dict[str, Any]) -> Dict[str, Any]:
        scores = {}
        
        basic_info = data.get("basic_info", {})
        if "experience_years" in basic_info:
            scores["experience_level"] = min(basic_info["experience_years"], 10)
        
        vision_info = data.get("vision_info", {})
        if "philosophy" in vision_info:
            philosophy_map = {
                "organic": 80,
                "tech": 20,
                "balanced": 50,
                "business": 30
            }
            scores["philosophy_score"] = philosophy_map.get(vision_info["philosophy"], 50)
        
        partnership = data.get("partnership", {})
        if "mentorship_need" in partnership:
            need_map = {
                "high": 5,
                "medium": 3,
                "low": 1,
                "none": 0
            }
            scores["mentorship_need_level"] = need_map.get(partnership["mentorship_need"], 3)
        
        finance = data.get("finance", {})
        if "capital" in finance:
            scores["capital_min"] = finance["capital"].get("min", 0)
            scores["capital_max"] = finance["capital"].get("max", 0)
        
        if "timeline" in finance:
            timeline_map = {
                "immediate": 3,
                "6months": 6,
                "1year": 12,
                "2years": 24,
                "3years+": 36
            }
            scores["timeline_months"] = timeline_map.get(finance["timeline"], 12)
        
        return scores
    
    @staticmethod
    async def save_senior_profile(
        db: AsyncSession, 
        user_id: UUID,
        data: Dict[str, Any]
    ) -> SeniorProfileV2:
        stmt = select(SeniorProfileV2).where(SeniorProfileV2.user_id == user_id)
        result = await db.execute(stmt)
        profile = result.scalar_one_or_none()
        
        scores = SurveyV2Service.calculate_scores_from_senior_survey(data)
        
        if profile:
            profile.basic_info = data.get("basic_info", {})
            profile.successor_pref = data.get("successor_pref", {})
            profile.conditions = data.get("conditions", {})
            profile.vision = data.get("vision", {})
            
            for key, value in scores.items():
                setattr(profile, key, value)
        else:
            profile = SeniorProfileV2(
                user_id=user_id,
                basic_info=data.get("basic_info", {}),
                successor_pref=data.get("successor_pref", {}),
                conditions=data.get("conditions", {}),
                vision=data.get("vision", {}),
                **scores
            )
            db.add(profile)
        
        await db.commit()
        await db.refresh(profile)
        return profile
    
    @staticmethod
    async def save_youth_profile(
        db: AsyncSession,
        user_id: UUID,
        data: Dict[str, Any]
    ) -> YouthProfileV2:
        stmt = select(YouthProfileV2).where(YouthProfileV2.user_id == user_id)
        result = await db.execute(stmt)
        profile = result.scalar_one_or_none()
        
        scores = SurveyV2Service.calculate_scores_from_youth_survey(data)
        
        if profile:
            profile.basic_info = data.get("basic_info", {})
            profile.vision_info = data.get("vision_info", {})
            profile.partnership = data.get("partnership", {})
            profile.finance = data.get("finance", {})
            
            for key, value in scores.items():
                setattr(profile, key, value)
        else:
            profile = YouthProfileV2(
                user_id=user_id,
                basic_info=data.get("basic_info", {}),
                vision_info=data.get("vision_info", {}),
                partnership=data.get("partnership", {}),
                finance=data.get("finance", {}),
                **scores
            )
            db.add(profile)
        
        await db.commit()
        await db.refresh(profile)
        return profile
    
    @staticmethod
    async def save_vision_profile(
        db: AsyncSession,
        user_id: UUID,
        data: Dict[str, Any]
    ) -> YouthVisionProfile:
        stmt = select(YouthVisionProfile).where(YouthVisionProfile.user_id == user_id)
        result = await db.execute(stmt)
        profile = result.scalar_one_or_none()
        
        if profile:
            profile.goal = data.get("goal")
            profile.experience = data.get("experience")
            profile.skills = data.get("skills", [])
            profile.vision = data.get("vision")
            profile.conditions = data.get("conditions", {})
            profile.profile_photos = data.get("profile_photos", [])
            profile.greeting = data.get("greeting")
            profile.completed = True
        else:
            profile = YouthVisionProfile(
                user_id=user_id,
                goal=data.get("goal"),
                experience=data.get("experience"),
                skills=data.get("skills", []),
                vision=data.get("vision"),
                conditions=data.get("conditions", {}),
                profile_photos=data.get("profile_photos", []),
                greeting=data.get("greeting"),
                completed=True
            )
            db.add(profile)
        
        await db.commit()
        await db.refresh(profile)
        return profile
    
    @staticmethod
    async def get_senior_profile(db: AsyncSession, user_id: UUID) -> Optional[SeniorProfileV2]:
        stmt = select(SeniorProfileV2).where(SeniorProfileV2.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_youth_profile(db: AsyncSession, user_id: UUID) -> Optional[YouthProfileV2]:
        stmt = select(YouthProfileV2).where(YouthProfileV2.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_vision_profile(db: AsyncSession, user_id: UUID) -> Optional[YouthVisionProfile]:
        stmt = select(YouthVisionProfile).where(YouthVisionProfile.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()