from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc
from uuid import UUID
import math
import json
import numpy as np

from app.models.user import User, UserType
from app.models.profile import SeniorProfile, YouthProfile
from app.models.matching import MatchingScore, Match, MatchStatus
from app.services.embedding import EmbeddingService
from app.services.gemini import GeminiService


class MatchingEngine:
    
    WEIGHTS = {
        'philosophy': 0.30,
        'experience': 0.20,
        'financial': 0.20,
        'timeline': 0.15,
        'mentorship': 0.15
    }
    
    @staticmethod
    def calculate_philosophy_compatibility(senior_score: float, youth_score: float) -> float:
        diff = abs(senior_score - youth_score)
        if diff <= 10:
            return 100.0
        elif diff <= 30:
            return 100.0 - (diff - 10) * 2
        else:
            return max(0, 60.0 - (diff - 30))
    
    @staticmethod
    def calculate_experience_compatibility(
        senior_required: Optional[int], 
        youth_level: Optional[int]
    ) -> float:
        if senior_required is None or youth_level is None:
            return 50.0
        
        if youth_level >= senior_required:
            return 100.0
        
        gap = senior_required - youth_level
        if gap <= 1:
            return 80.0
        elif gap <= 2:
            return 60.0
        elif gap <= 3:
            return 40.0
        else:
            return 20.0
    
    @staticmethod
    def calculate_financial_compatibility(
        senior_min: Optional[int],
        senior_max: Optional[int],
        youth_min: Optional[int],
        youth_max: Optional[int]
    ) -> float:
        if not all([senior_min, senior_max, youth_min, youth_max]):
            return 50.0
        
        overlap_min = max(senior_min, youth_min)
        overlap_max = min(senior_max, youth_max)
        
        if overlap_max < overlap_min:
            return 0.0
        
        senior_range = senior_max - senior_min
        youth_range = youth_max - youth_min
        overlap_range = overlap_max - overlap_min
        
        if senior_range == 0 or youth_range == 0:
            return 50.0
        
        overlap_ratio = (overlap_range / senior_range + overlap_range / youth_range) / 2
        return min(100.0, overlap_ratio * 100)
    
    @staticmethod
    def calculate_timeline_compatibility(
        senior_months: Optional[int],
        youth_months: Optional[int]
    ) -> float:
        if senior_months is None or youth_months is None:
            return 50.0
        
        diff = abs(senior_months - youth_months)
        
        if diff <= 3:
            return 100.0
        elif diff <= 6:
            return 80.0
        elif diff <= 12:
            return 60.0
        elif diff <= 24:
            return 40.0
        else:
            return 20.0
    
    @staticmethod
    def calculate_mentorship_compatibility(
        senior_willingness: Optional[bool],
        youth_need_level: Optional[int]
    ) -> float:
        if senior_willingness is None or youth_need_level is None:
            return 50.0
        
        if senior_willingness:
            if youth_need_level >= 4:
                return 100.0
            elif youth_need_level >= 2:
                return 80.0
            else:
                return 60.0
        else:
            if youth_need_level <= 1:
                return 100.0
            elif youth_need_level <= 3:
                return 60.0
            else:
                return 20.0
    
    @staticmethod
    def calculate_location_bonus(
        senior_location: Optional[str],
        youth_location: Optional[str]
    ) -> float:
        if not senior_location or not youth_location:
            return 0.0
        
        senior_parts = senior_location.lower().split()
        youth_parts = youth_location.lower().split()
        
        common_parts = set(senior_parts) & set(youth_parts)
        
        if len(common_parts) >= 2:
            return 10.0
        elif len(common_parts) >= 1:
            return 5.0
        return 0.0
    
    @staticmethod
    def calculate_crop_bonus(
        senior_crop: Optional[str],
        youth_crop: Optional[str]
    ) -> float:
        if not senior_crop or not youth_crop:
            return 0.0
        
        senior_crops = set(senior_crop.lower().split(','))
        youth_crops = set(youth_crop.lower().split(','))
        
        if senior_crops & youth_crops:
            return 5.0
        return 0.0
    
    @staticmethod
    def get_ai_recommendation(sci_score: float) -> str:
        if sci_score >= 80:
            return "Perfect Match"
        elif sci_score >= 70:
            return "Excellent Match"
        elif sci_score >= 60:
            return "Good Match"
        elif sci_score >= 50:
            return "Fair Match"
        else:
            return "Needs Consideration"
    
    @staticmethod
    def generate_insights(
        philosophy: float,
        experience: float,
        financial: float,
        timeline: float,
        mentorship: float
    ) -> str:
        insights = []
        
        if philosophy >= 80:
            insights.append("농업 철학이 매우 잘 맞습니다")
        elif philosophy <= 40:
            insights.append("농업 철학 차이로 갈등 가능성이 있습니다")
        
        if experience >= 80:
            insights.append("경험 수준이 적합합니다")
        elif experience <= 40:
            insights.append("경험 차이를 보완할 방안이 필요합니다")
        
        if financial >= 80:
            insights.append("재정 조건이 잘 맞습니다")
        elif financial <= 40:
            insights.append("재정 조건 조율이 필요합니다")
        
        if timeline >= 80:
            insights.append("승계 시기가 일치합니다")
        elif timeline <= 40:
            insights.append("승계 시기 조정이 필요합니다")
        
        if mentorship >= 80:
            insights.append("멘토십 기대가 일치합니다")
        elif mentorship <= 40:
            insights.append("멘토십 기대 차이가 있습니다")
        
        return ". ".join(insights) if insights else "전반적으로 균형잡힌 매칭입니다"
    
    @staticmethod
    async def calculate_match(
        db: AsyncSession,
        senior_profile: SeniorProfile,
        youth_profile: YouthProfile
    ) -> MatchingScore:
        philosophy = MatchingEngine.calculate_philosophy_compatibility(
            senior_profile.philosophy_score or 50,
            youth_profile.philosophy_score or 50
        )
        
        experience = MatchingEngine.calculate_experience_compatibility(
            senior_profile.experience_required,
            youth_profile.experience_level
        )
        
        financial = MatchingEngine.calculate_financial_compatibility(
            senior_profile.price_min,
            senior_profile.price_max,
            youth_profile.capital_min,
            youth_profile.capital_max
        )
        
        timeline = MatchingEngine.calculate_timeline_compatibility(
            senior_profile.timeline_months,
            youth_profile.timeline_months
        )
        
        mentorship = MatchingEngine.calculate_mentorship_compatibility(
            senior_profile.mentoring_willingness,
            youth_profile.mentorship_need_level
        )
        
        location_bonus = MatchingEngine.calculate_location_bonus(
            senior_profile.basic_info.get("location") if senior_profile.basic_info else None,
            youth_profile.basic_info.get("location") if youth_profile.basic_info else None
        )
        
        crop_bonus = MatchingEngine.calculate_crop_bonus(
            senior_profile.basic_info.get("main_crop") if senior_profile.basic_info else None,
            youth_profile.basic_info.get("desired_crop") if youth_profile.basic_info else None
        )
        
        sci_total = (
            philosophy * MatchingEngine.WEIGHTS['philosophy'] +
            experience * MatchingEngine.WEIGHTS['experience'] +
            financial * MatchingEngine.WEIGHTS['financial'] +
            timeline * MatchingEngine.WEIGHTS['timeline'] +
            mentorship * MatchingEngine.WEIGHTS['mentorship']
        )
        
        sci_total = min(100, sci_total + location_bonus + crop_bonus)
        
        stmt = select(MatchingScore).where(
            and_(
                MatchingScore.senior_id == senior_profile.user_id,
                MatchingScore.youth_id == youth_profile.user_id
            )
        )
        result = await db.execute(stmt)
        match_score = result.scalar_one_or_none()
        
        if match_score:
            match_score.sci_total_score = sci_total
            match_score.philosophy_score = philosophy
            match_score.experience_score = experience
            match_score.financial_score = financial
            match_score.timeline_score = timeline
            match_score.mentorship_score = mentorship
            match_score.location_bonus = location_bonus
            match_score.crop_bonus = crop_bonus
            match_score.ai_recommendation = MatchingEngine.get_ai_recommendation(sci_total)
            match_score.ai_insights = MatchingEngine.generate_insights(
                philosophy, experience, financial, timeline, mentorship
            )
        else:
            match_score = MatchingScore(
                senior_id=senior_profile.user_id,
                youth_id=youth_profile.user_id,
                sci_total_score=sci_total,
                philosophy_score=philosophy,
                experience_score=experience,
                financial_score=financial,
                timeline_score=timeline,
                mentorship_score=mentorship,
                location_bonus=location_bonus,
                crop_bonus=crop_bonus,
                ai_recommendation=MatchingEngine.get_ai_recommendation(sci_total),
                ai_insights=MatchingEngine.generate_insights(
                    philosophy, experience, financial, timeline, mentorship
                ),
                mutual_interest="none"
            )
            db.add(match_score)
        
        await db.commit()
        await db.refresh(match_score)
        return match_score
    
    @staticmethod
    async def find_matches_for_user(
        db: AsyncSession,
        user_id: UUID,
        user_type: UserType,
        limit: int = 10
    ) -> List[MatchingScore]:
        if user_type == UserType.SENIOR:
            stmt = select(YouthProfile)
            result = await db.execute(stmt)
            youth_profiles = result.scalars().all()
            
            senior_stmt = select(SeniorProfile).where(SeniorProfile.user_id == user_id)
            senior_result = await db.execute(senior_stmt)
            senior_profile = senior_result.scalar_one_or_none()
            
            if not senior_profile:
                return []
            
            matches = []
            for youth_profile in youth_profiles:
                match = await MatchingEngine.calculate_match(db, senior_profile, youth_profile)
                matches.append(match)
        
        else:
            stmt = select(SeniorProfile)
            result = await db.execute(stmt)
            senior_profiles = result.scalars().all()
            
            youth_stmt = select(YouthProfile).where(YouthProfile.user_id == user_id)
            youth_result = await db.execute(youth_stmt)
            youth_profile = youth_result.scalar_one_or_none()
            
            if not youth_profile:
                return []
            
            matches = []
            for senior_profile in senior_profiles:
                match = await MatchingEngine.calculate_match(db, senior_profile, youth_profile)
                matches.append(match)
        
        matches.sort(key=lambda x: x.sci_total_score, reverse=True)
        
        return matches[:limit]
    
    @staticmethod
    async def create_or_update_match(
        db: AsyncSession,
        senior_profile: SeniorProfile,
        youth_profile: YouthProfile,
        persona_types: Optional[Dict[str, str]] = None
    ) -> Match:
        philosophy = MatchingEngine.calculate_philosophy_compatibility(
            senior_profile.philosophy_score or 50,
            youth_profile.philosophy_score or 50
        )
        
        business = MatchingEngine.calculate_experience_compatibility(
            senior_profile.experience_required,
            youth_profile.experience_level
        )
        
        finance = MatchingEngine.calculate_financial_compatibility(
            senior_profile.price_min,
            senior_profile.price_max,
            youth_profile.capital_min,
            youth_profile.capital_max
        )
        
        mentorship = MatchingEngine.calculate_mentorship_compatibility(
            senior_profile.mentoring_willingness,
            youth_profile.mentorship_need_level
        )
        
        sci_score = (
            philosophy * 0.4 +
            business * 0.2 +
            mentorship * 0.2 +
            finance * 0.2
        )
        
        location_distance = MatchingEngine.calculate_location_bonus(
            senior_profile.basic_info.get("location") if senior_profile.basic_info else None,
            youth_profile.basic_info.get("location") if youth_profile.basic_info else None
        )
        
        crop_match = bool(MatchingEngine.calculate_crop_bonus(
            senior_profile.basic_info.get("main_crop") if senior_profile.basic_info else None,
            youth_profile.basic_info.get("desired_crop") if youth_profile.basic_info else None
        ))
        
        stmt = select(Match).where(
            and_(
                Match.senior_id == senior_profile.user_id,
                Match.youth_id == youth_profile.user_id
            )
        )
        result = await db.execute(stmt)
        match = result.scalar_one_or_none()
        
        if match:
            match.sci_score = sci_score
            match.philosophy_compatibility = philosophy
            match.business_compatibility = business
            match.mentorship_compatibility = mentorship
            match.finance_compatibility = finance
            match.location_distance_km = location_distance * 10
            match.crop_match = crop_match
            match.ai_recommendation = MatchingEngine.get_ai_recommendation(sci_score)
            match.compatibility_details = MatchingEngine.generate_insights(
                philosophy, business, finance, 
                MatchingEngine.calculate_timeline_compatibility(
                    senior_profile.timeline_months,
                    youth_profile.timeline_months
                ), 
                mentorship
            )
            if persona_types:
                match.senior_persona_type = persona_types.get("senior")
                match.youth_persona_type = persona_types.get("youth")
        else:
            match = Match(
                senior_id=senior_profile.user_id,
                youth_id=youth_profile.user_id,
                sci_score=sci_score,
                philosophy_compatibility=philosophy,
                business_compatibility=business,
                mentorship_compatibility=mentorship,
                finance_compatibility=finance,
                status=MatchStatus.PENDING,
                senior_persona_type=persona_types.get("senior") if persona_types else None,
                youth_persona_type=persona_types.get("youth") if persona_types else None,
                location_distance_km=location_distance * 10,
                crop_match=crop_match,
                ai_recommendation=MatchingEngine.get_ai_recommendation(sci_score),
                compatibility_details=MatchingEngine.generate_insights(
                    philosophy, business, finance,
                    MatchingEngine.calculate_timeline_compatibility(
                        senior_profile.timeline_months,
                        youth_profile.timeline_months
                    ),
                    mentorship
                )
            )
            db.add(match)
        
        await db.commit()
        await db.refresh(match)
        return match
    
    @staticmethod
    async def get_recommendations(
        db: AsyncSession,
        user_id: UUID,
        user_type: UserType,
        limit: int = 10
    ) -> List[Match]:
        if user_type == UserType.SENIOR:
            stmt = select(Match).where(
                Match.senior_id == user_id
            ).order_by(desc(Match.sci_score)).limit(limit)
        else:
            stmt = select(Match).where(
                Match.youth_id == user_id
            ).order_by(desc(Match.sci_score)).limit(limit)
        
        result = await db.execute(stmt)
        matches = result.scalars().all()
        
        return matches
    
    @staticmethod
    async def get_hybrid_recommendations(
        db: AsyncSession,
        user_id: UUID,
        user_type: UserType,
        limit: int = 10,
        min_embedding_similarity: float = 0.6,
        embedding_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """하이브리드 매칭: 임베딩 유사도 + SCI 점수"""
        
        # 1. 사용자 프로필 가져오기
        if user_type == UserType.SENIOR:
            user_result = await db.execute(
                select(SeniorProfile).where(SeniorProfile.user_id == user_id)
            )
            user_profile = user_result.scalar_one_or_none()
            target_model = YouthProfile
        else:
            user_result = await db.execute(
                select(YouthProfile).where(YouthProfile.user_id == user_id)
            )
            user_profile = user_result.scalar_one_or_none()
            target_model = SeniorProfile
        
        if not user_profile or not user_profile.embedding:
            # 임베딩이 없으면 기존 SCI 매칭으로 대체
            matches = await MatchingEngine.get_recommendations(db, user_id, user_type, limit)
            return [{"match": match, "hybrid_score": match.sci_score} for match in matches]
        
        # 2. 임베딩 기반 후보 필터링 (1차 필터)
        candidates_result = await db.execute(
            select(target_model).where(target_model.embedding != None)
        )
        candidates = candidates_result.scalars().all()
        
        embedding_scores = []
        for candidate in candidates:
            if candidate.embedding:
                similarity = EmbeddingService.calculate_similarity(
                    user_profile.embedding,
                    candidate.embedding
                )
                if similarity >= min_embedding_similarity:
                    embedding_scores.append({
                        "profile": candidate,
                        "embedding_similarity": similarity
                    })
        
        # 3. 상위 후보들에 대해 SCI 계산 (2차 계산)
        embedding_scores.sort(key=lambda x: x["embedding_similarity"], reverse=True)
        top_candidates = embedding_scores[:limit * 2]  # 2배수로 후보 선정
        
        hybrid_results = []
        for candidate_info in top_candidates:
            candidate = candidate_info["profile"]
            
            # SCI 점수 계산
            if user_type == UserType.SENIOR:
                match_score = await MatchingEngine.calculate_match(db, user_profile, candidate)
            else:
                match_score = await MatchingEngine.calculate_match(db, candidate, user_profile)
            
            # 하이브리드 점수 계산
            hybrid_score = (
                match_score.sci_total_score * (1 - embedding_weight) +
                candidate_info["embedding_similarity"] * 100 * embedding_weight
            )
            
            # Gemini로 매칭 설명 생성
            explanation = None
            if user_profile.profile_text and candidate.profile_text:
                explanation = GeminiService.generate_match_explanation(
                    senior_profile=user_profile.__dict__ if user_type == UserType.SENIOR else candidate.__dict__,
                    youth_profile=candidate.__dict__ if user_type == UserType.SENIOR else user_profile.__dict__,
                    sci_score=match_score.sci_total_score,
                    compatibility_details={
                        "philosophy": match_score.philosophy_score,
                        "business": match_score.experience_score,
                        "mentorship": match_score.mentorship_score,
                        "finance": match_score.financial_score
                    }
                )
            
            hybrid_results.append({
                "candidate_id": candidate.user_id,
                "candidate_profile": candidate,
                "sci_score": match_score.sci_total_score,
                "embedding_similarity": candidate_info["embedding_similarity"],
                "hybrid_score": hybrid_score,
                "compatibility_details": {
                    "philosophy": match_score.philosophy_score,
                    "experience": match_score.experience_score,
                    "financial": match_score.financial_score,
                    "timeline": match_score.timeline_score,
                    "mentorship": match_score.mentorship_score
                },
                "ai_explanation": explanation
            })
        
        # 4. 하이브리드 점수로 정렬
        hybrid_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        
        return hybrid_results[:limit]