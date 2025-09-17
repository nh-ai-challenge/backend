from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User


async def get_current_user(
    user_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> User:
    from starlette.requests import Request
    from fastapi import Request as FastAPIRequest
    import inspect
    
    frame = inspect.currentframe()
    request = None
    
    while frame:
        local_vars = frame.f_locals
        for var_name, var_value in local_vars.items():
            if isinstance(var_value, Request) or isinstance(var_value, FastAPIRequest):
                request = var_value
                break
        if request:
            break
        frame = frame.f_back
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user