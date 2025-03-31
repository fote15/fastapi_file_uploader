from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.db.session import get_db
from app.db.models import User
from app.core.security import create_access_token, pwd_context, create_refresh_token
import httpx

router = APIRouter()

@router.get("/link")
async def get_yandex_auth_link():
    return {"auth_url": f"{settings.YANDEX_AUTH_URL}?response_type=code&client_id={settings.YANDEX_CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}"}


@router.get("/")
async def yandex_auth(code: str, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET
            }
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to authenticate with Yandex")
    token_data = response.json()
    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(
            settings.YANDEX_USER_INFO_URL,
            headers={"Authorization": f"OAuth {token_data['access_token']}"}
        )

    if user_info_response.status_code != 200:
        raise HTTPException(status_code=user_info_response.status_code, detail="Failed to fetch user info")
    user_info = user_info_response.json()

    result = await db.execute(select(User).where(User.username == user_info["login"]))
    user = result.scalars().first()

    if not user:
        user = User(username=user_info["login"], email=user_info.get("default_email", ""))
        db.add(user)
        await db.commit()

    access_token = create_access_token({"sub": user.username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token({"sub": user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

