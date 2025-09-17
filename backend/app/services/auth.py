from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        user_dict = user_data.model_dump()
        password = user_dict.pop('password')
        
        db_user = User(
            **user_dict,
            password_hash=AuthService.hash_password(password)
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> Optional[User]:
        query = select(User).where(User.username == login_data.username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not AuthService.verify_password(login_data.password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()