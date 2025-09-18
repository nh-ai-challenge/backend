from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.models.user import User, UserType
from app.models.profile import SeniorProfile, YouthProfile
from app.schemas.survey import (
    ProfileTextUpdate,
    ProfileTextResponse,
    SeniorProfileResponse,
    YouthProfileResponse
)
from app.services.embedding import EmbeddingService
from app.services.gemini import GeminiService
from app.api.deps import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/me", response_model_exclude_none=True)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """현재 사용자의 프로필 조회"""
    
    if current_user.user_type == UserType.SENIOR:
        result = await db.execute(
            select(SeniorProfile).where(SeniorProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise HTTPException(status_code=404, detail="프로필이 없습니다")
        
        return SeniorProfileResponse.from_orm(profile)
    else:
        result = await db.execute(
            select(YouthProfile).where(YouthProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise HTTPException(status_code=404, detail="프로필이 없습니다")
        
        return YouthProfileResponse.from_orm(profile)


@router.put("/me/profile-text", response_model=ProfileTextResponse)
async def update_profile_text(
    request: ProfileTextUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """프로필 텍스트 업데이트 및 임베딩 생성"""
    
    profile = await EmbeddingService.update_profile_embedding_async(
        db=db,
        user_id=str(current_user.id),
        user_type=current_user.user_type,
        profile_text=request.profile_text
    )
    
    if not profile:
        raise HTTPException(status_code=404, detail="프로필이 없습니다")
    
    return ProfileTextResponse(
        profile_text=profile.profile_text,
        embedding_updated_at=profile.embedding_updated_at,
        has_embedding=profile.embedding is not None,
        message="프로필 텍스트가 업데이트되고 임베딩이 생성되었습니다"
    )


@router.get("/me/profile-summary")
async def get_profile_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """AI가 생성한 프로필 요약 조회"""
    
    if current_user.user_type == UserType.SENIOR:
        result = await db.execute(
            select(SeniorProfile).where(SeniorProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
    else:
        result = await db.execute(
            select(YouthProfile).where(YouthProfile.user_id == current_user.id)
        )
        profile = result.scalar_one_or_none()
    
    if not profile or not profile.profile_text:
        raise HTTPException(
            status_code=404,
            detail="프로필 텍스트가 없습니다. 먼저 프로필을 작성해주세요."
        )
    
    summary = GeminiService.generate_profile_summary(
        profile.profile_text,
        current_user.user_type.value
    )
    
    if not summary:
        raise HTTPException(
            status_code=503,
            detail="AI 서비스가 일시적으로 사용할 수 없습니다"
        )
    
    return {
        "profile_text": profile.profile_text,
        "ai_summary": summary,
        "user_type": current_user.user_type.value
    }


@router.get("/{user_id}")
async def get_user_profile(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """특정 사용자의 프로필 조회 (매칭된 경우에만)"""
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    target_user = result.scalar_one_or_none()
    
    if not target_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # TODO: 매칭 권한 체크 로직 추가
    # 현재는 임시로 모든 프로필 조회 가능
    
    if target_user.user_type == UserType.SENIOR:
        result = await db.execute(
            select(SeniorProfile).where(SeniorProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise HTTPException(status_code=404, detail="프로필이 없습니다")
        
        return SeniorProfileResponse.from_orm(profile)
    else:
        result = await db.execute(
            select(YouthProfile).where(YouthProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            raise HTTPException(status_code=404, detail="프로필이 없습니다")
        
        return YouthProfileResponse.from_orm(profile)