from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.core.database import get_db
from app.models.user import User, UserType
from app.models.matching import Match, MatchStatus
from app.models.profile import SeniorProfile, YouthProfile
from app.api.deps import get_current_user
from app.schemas.matching import (
    MatchResponse,
    MatchDetailResponse,
    MatchCalculateRequest,
    MatchCalculateResponse,
    MatchStatusUpdate
)
from app.services.matching import MatchingEngine
from app.services.gemini import GeminiService

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/recommendations/hybrid")
async def get_hybrid_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    min_similarity: float = Query(0.6, ge=0.0, le=1.0, description="Minimum embedding similarity"),
    embedding_weight: float = Query(0.3, ge=0.0, le=1.0, description="Weight for embedding score")
) -> List[Dict[str, Any]]:
    """하이브리드 매칭: 텍스트 유사도 + SCI 점수 결합"""
    
    recommendations = await MatchingEngine.get_hybrid_recommendations(
        db=db,
        user_id=current_user.id,
        user_type=current_user.user_type,
        limit=limit,
        min_embedding_similarity=min_similarity,
        embedding_weight=embedding_weight
    )
    
    if not recommendations:
        # 프로필 확인
        if current_user.user_type == UserType.SENIOR:
            profile_check = await db.execute(
                select(SeniorProfile).where(SeniorProfile.user_id == current_user.id)
            )
            profile = profile_check.scalar_one_or_none()
        else:
            profile_check = await db.execute(
                select(YouthProfile).where(YouthProfile.user_id == current_user.id)
            )
            profile = profile_check.scalar_one_or_none()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="프로필을 먼저 작성해주세요"
            )
        elif not profile.profile_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="프로필 텍스트를 작성해야 하이브리드 매칭을 사용할 수 있습니다"
            )
        else:
            return []
    
    # 응답 형식 정리
    results = []
    for rec in recommendations:
        results.append({
            "candidate_id": str(rec["candidate_id"]),
            "hybrid_score": round(rec["hybrid_score"], 2),
            "sci_score": round(rec["sci_score"], 2),
            "text_similarity": round(rec["embedding_similarity"] * 100, 2),
            "compatibility": {
                "philosophy": round(rec["compatibility_details"]["philosophy"], 1),
                "experience": round(rec["compatibility_details"]["experience"], 1),
                "financial": round(rec["compatibility_details"]["financial"], 1),
                "timeline": round(rec["compatibility_details"]["timeline"], 1),
                "mentorship": round(rec["compatibility_details"]["mentorship"], 1)
            },
            "ai_explanation": rec.get("ai_explanation", "매칭 설명을 생성할 수 없습니다")
        })
    
    return results


@router.get("/recommendations", response_model=List[MatchResponse])
async def get_match_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations to return")
):
    matches = await MatchingEngine.get_recommendations(
        db, current_user.id, current_user.user_type, limit
    )
    
    if not matches:
        if current_user.user_type == UserType.SENIOR:
            profile_check = await db.execute(
                select(SeniorProfile).where(SeniorProfile.user_id == current_user.id)
            )
            if not profile_check.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Please complete your profile first"
                )
        else:
            profile_check = await db.execute(
                select(YouthProfile).where(YouthProfile.user_id == current_user.id)
            )
            if not profile_check.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Please complete your profile first"
                )
        
        await MatchingEngine.find_matches_for_user(
            db, current_user.id, current_user.user_type, limit
        )
        
        matches = await MatchingEngine.get_recommendations(
            db, current_user.id, current_user.user_type, limit
        )
    
    return [
        MatchResponse(
            match_id=match.id,
            partner_id=match.youth_id if current_user.user_type == UserType.SENIOR else match.senior_id,
            partner_type="youth" if current_user.user_type == UserType.SENIOR else "senior",
            sci_score=match.sci_score,
            philosophy_compatibility=match.philosophy_compatibility,
            business_compatibility=match.business_compatibility,
            mentorship_compatibility=match.mentorship_compatibility,
            finance_compatibility=match.finance_compatibility,
            status=match.status,
            ai_recommendation=match.ai_recommendation,
            created_at=match.created_at
        )
        for match in matches
    ]


@router.get("/{match_id}")
async def get_match_detail(
    match_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    generate_explanation: bool = Query(True, description="AI 설명 생성 여부")
):
    stmt = select(Match).where(
        and_(
            Match.id == match_id,
            or_(
                Match.senior_id == current_user.id,
                Match.youth_id == current_user.id
            )
        )
    )
    
    result = await db.execute(stmt)
    match = result.scalar_one_or_none()
    
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    partner_id = match.youth_id if match.senior_id == current_user.id else match.senior_id
    partner_stmt = select(User).where(User.id == partner_id)
    partner_result = await db.execute(partner_stmt)
    partner = partner_result.scalar_one()
    
    # AI 설명 생성 (선택적)
    ai_explanation = None
    if generate_explanation:
        # 시니어와 청년 프로필 가져오기
        senior_stmt = select(SeniorProfile).where(SeniorProfile.user_id == match.senior_id)
        senior_result = await db.execute(senior_stmt)
        senior_profile = senior_result.scalar_one_or_none()
        
        youth_stmt = select(YouthProfile).where(YouthProfile.user_id == match.youth_id)
        youth_result = await db.execute(youth_stmt)
        youth_profile = youth_result.scalar_one_or_none()
        
        if senior_profile and youth_profile:
            # Gemini로 매칭 설명 생성
            ai_explanation = GeminiService.generate_match_explanation(
                senior_profile={
                    "basic_info": senior_profile.basic_info,
                    "successor_pref": senior_profile.successor_pref,
                    "conditions": senior_profile.conditions,
                    "vision": senior_profile.vision,
                    "profile_text": senior_profile.profile_text
                },
                youth_profile={
                    "basic_info": youth_profile.basic_info,
                    "vision_info": youth_profile.vision_info,
                    "partnership": youth_profile.partnership,
                    "finance": youth_profile.finance,
                    "profile_text": youth_profile.profile_text
                },
                sci_score=match.sci_score,
                compatibility_details={
                    "philosophy": match.philosophy_compatibility,
                    "business": match.business_compatibility,
                    "mentorship": match.mentorship_compatibility,
                    "finance": match.finance_compatibility
                }
            )
    
    return {
        "match_id": match.id,
        "partner_id": partner.id,
        "partner_name": partner.name,
        "partner_type": partner.user_type.value,
        "sci_score": match.sci_score,
        "compatibility": {
            "philosophy": match.philosophy_compatibility,
            "business": match.business_compatibility,
            "mentorship": match.mentorship_compatibility,
            "finance": match.finance_compatibility
        },
        "persona_types": {
            "senior": match.senior_persona_type,
            "youth": match.youth_persona_type
        },
        "location_distance_km": match.location_distance_km,
        "crop_match": match.crop_match,
        "basic_insights": match.compatibility_details,
        "ai_level": match.ai_recommendation,
        "ai_explanation": ai_explanation or "AI 설명을 생성할 수 없습니다",
        "status": match.status.value,
        "created_at": match.created_at,
        "updated_at": match.updated_at
    }


@router.post("/calculate")
async def calculate_match_score(
    request: MatchCalculateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    generate_explanation: bool = Query(True, description="AI 설명 생성 여부")
):
    if request.senior_id == request.youth_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot calculate match with yourself"
        )
    
    if current_user.id not in [request.senior_id, request.youth_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only calculate matches involving yourself"
        )
    
    senior_stmt = select(SeniorProfile).where(SeniorProfile.user_id == request.senior_id)
    senior_result = await db.execute(senior_stmt)
    senior_profile = senior_result.scalar_one_or_none()
    
    if not senior_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Senior profile not found"
        )
    
    youth_stmt = select(YouthProfile).where(YouthProfile.user_id == request.youth_id)
    youth_result = await db.execute(youth_stmt)
    youth_profile = youth_result.scalar_one_or_none()
    
    if not youth_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Youth profile not found"
        )
    
    match = await MatchingEngine.create_or_update_match(
        db, senior_profile, youth_profile
    )
    
    # AI 설명 생성
    ai_explanation = None
    if generate_explanation and senior_profile and youth_profile:
        ai_explanation = GeminiService.generate_match_explanation(
            senior_profile={
                "basic_info": senior_profile.basic_info,
                "successor_pref": senior_profile.successor_pref,
                "conditions": senior_profile.conditions,
                "vision": senior_profile.vision,
                "profile_text": senior_profile.profile_text
            },
            youth_profile={
                "basic_info": youth_profile.basic_info,
                "vision_info": youth_profile.vision_info,
                "partnership": youth_profile.partnership,
                "finance": youth_profile.finance,
                "profile_text": youth_profile.profile_text
            },
            sci_score=match.sci_score,
            compatibility_details={
                "philosophy": match.philosophy_compatibility,
                "business": match.business_compatibility,
                "mentorship": match.mentorship_compatibility,
                "finance": match.finance_compatibility
            }
        )
    
    return {
        "match_id": match.id,
        "senior_id": match.senior_id,
        "youth_id": match.youth_id,
        "sci_score": match.sci_score,
        "compatibility": {
            "philosophy": match.philosophy_compatibility,
            "business": match.business_compatibility,
            "mentorship": match.mentorship_compatibility,
            "finance": match.finance_compatibility
        },
        "ai_level": match.ai_recommendation,
        "basic_insights": match.compatibility_details,
        "ai_explanation": ai_explanation or "매칭 설명을 생성할 수 없습니다",
        "status": match.status.value,
        "created_at": match.created_at
    }


@router.put("/{match_id}/status")
async def update_match_status(
    match_id: UUID,
    status_update: MatchStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Match).where(
        and_(
            Match.id == match_id,
            or_(
                Match.senior_id == current_user.id,
                Match.youth_id == current_user.id
            )
        )
    )
    
    result = await db.execute(stmt)
    match = result.scalar_one_or_none()
    
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    match.status = status_update.status
    await db.commit()
    
    return {"message": f"Match status updated to {status_update.status}"}


@router.get("/")
async def get_all_matches(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    status_filter: Optional[MatchStatus] = None
):
    if current_user.user_type == UserType.SENIOR:
        stmt = select(Match).where(Match.senior_id == current_user.id)
    else:
        stmt = select(Match).where(Match.youth_id == current_user.id)
    
    if status_filter:
        stmt = stmt.where(Match.status == status_filter)
    
    stmt = stmt.order_by(desc(Match.sci_score))
    
    result = await db.execute(stmt)
    matches = result.scalars().all()
    
    return [
        {
            "match_id": match.id,
            "sci_score": match.sci_score,
            "status": match.status,
            "ai_recommendation": match.ai_recommendation,
            "created_at": match.created_at
        }
        for match in matches
    ]