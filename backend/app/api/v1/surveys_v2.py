from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from uuid import UUID

from app.core.database import get_db
from app.models.user import User, UserType
from app.api.deps import get_current_user
from app.schemas.survey_v2 import (
    SeniorSurveySection,
    YouthSurveySection,
    VisionProfileRequest,
    SeniorProfileResponse,
    YouthProfileResponse,
    VisionProfileResponse,
    SurveySubmissionResult
)
from app.services.survey_v2 import SurveyV2Service

router = APIRouter(prefix="/surveys-v2", tags=["surveys-v2"])


@router.post("/senior", response_model=SurveySubmissionResult)
async def submit_senior_survey(
    data: SeniorSurveySection,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_type != UserType.SENIOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only senior users can submit senior surveys"
        )
    
    profile = await SurveyV2Service.save_senior_profile(
        db, current_user.id, data.model_dump()
    )
    
    return SurveySubmissionResult(
        profile_id=profile.id,
        philosophy_score=profile.philosophy_score or 50.0,
        experience_score=float(profile.experience_required * 20) if profile.experience_required else None,
        financial_score=float((profile.price_min + profile.price_max) / 20000) if profile.price_min else None,
        timeline_score=float(100 - (profile.timeline_months * 2.5)) if profile.timeline_months else None,
        mentorship_score=100.0 if profile.mentoring_willingness else 50.0,
        message="시니어 프로필이 성공적으로 저장되었습니다."
    )


@router.post("/youth", response_model=SurveySubmissionResult)
async def submit_youth_survey(
    data: YouthSurveySection,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_type != UserType.YOUTH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only youth users can submit youth surveys"
        )
    
    profile = await SurveyV2Service.save_youth_profile(
        db, current_user.id, data.model_dump()
    )
    
    return SurveySubmissionResult(
        profile_id=profile.id,
        philosophy_score=profile.philosophy_score or 50.0,
        experience_score=float(profile.experience_level * 10) if profile.experience_level else None,
        financial_score=float((profile.capital_min + profile.capital_max) / 20000) if profile.capital_min else None,
        timeline_score=float(100 - (profile.timeline_months * 2.5)) if profile.timeline_months else None,
        mentorship_score=float(profile.mentorship_need_level * 20) if profile.mentorship_need_level else None,
        message="청년 프로필이 성공적으로 저장되었습니다."
    )


@router.post("/vision-profile", response_model=VisionProfileResponse)
async def submit_vision_profile(
    data: VisionProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_type != UserType.YOUTH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only youth users can submit vision profiles"
        )
    
    profile = await SurveyV2Service.save_vision_profile(
        db, current_user.id, data.model_dump()
    )
    
    return VisionProfileResponse.model_validate(profile)


@router.get("/senior/profile", response_model=SeniorProfileResponse)
async def get_senior_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_type != UserType.SENIOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only senior users can access senior profiles"
        )
    
    profile = await SurveyV2Service.get_senior_profile(db, current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Senior profile not found"
        )
    
    return SeniorProfileResponse.model_validate(profile)


@router.get("/youth/profile", response_model=YouthProfileResponse)
async def get_youth_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_type != UserType.YOUTH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only youth users can access youth profiles"
        )
    
    profile = await SurveyV2Service.get_youth_profile(db, current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Youth profile not found"
        )
    
    return YouthProfileResponse.model_validate(profile)


@router.get("/vision-profile", response_model=VisionProfileResponse)
async def get_vision_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_type != UserType.YOUTH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only youth users can access vision profiles"
        )
    
    profile = await SurveyV2Service.get_vision_profile(db, current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vision profile not found"
        )
    
    return VisionProfileResponse.model_validate(profile)