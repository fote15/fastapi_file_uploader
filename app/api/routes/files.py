from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form
import shutil
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import User, AudioFile
from fastapi.security import OAuth2PasswordBearer
from app.services.files import sanitize_filename, generate_random_hash
from app.services.auth import get_current_user

router = APIRouter()
UPLOAD_FOLDER = Path("audio_files")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_audio(
    file: UploadFile = File(...),
    filename: str = Form(...),  # User provides a filename
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filename = sanitize_filename(filename)
    file_ext = Path(file.filename).suffix

    # Ensure filename uniqueness
    existing_file = await db.execute(
        AudioFile.__table__.select().where(AudioFile.filename == filename)
    )
    existing_file = existing_file.scalar_one_or_none()

    if existing_file:
        file_hash = generate_random_hash()
        filename = f"{filename}_{file_hash[:8]}{file_ext}"  # Append a short hash

    file_path = UPLOAD_FOLDER / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = AudioFile(
        filename=filename,  # Store user-provided or unique filename
        path=str(file_path),
        owner_id=current_user.id
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return {
        "original_filename": file.filename,
        "chosen_filename": filename,
        "path": new_file.path,
        "uploaded_by": current_user.username
    }


@router.get("/my-files/")
async def get_my_files(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(AudioFile).where(AudioFile.owner_id == current_user.id)
    result = await db.execute(query)
    files = result.scalars().all()

    if not files:
        return []

    return [
        {
            "filename": file.filename,
            "path": file.path,
            "uploaded_by": current_user.username
        }
        for file in files
    ]
