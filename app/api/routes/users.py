from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models import User
from app.services.auth import get_current_user
from app.api.schemas.user import UserResponse
router = APIRouter()

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute("SELECT * FROM users")
    return users.fetchall()



@router.get("/get-user/{user_id}/", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure the user is allowed to view this data (can be adjusted for admin or self-only view)
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to view this user.")

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.post("/users/delete/")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure only admins can delete users
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to delete users.")

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    await db.delete(user)
    await db.commit()

    return {"message": "User deleted successfully"}
