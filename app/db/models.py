from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    files = relationship("AudioFile", back_populates="owner")
    is_admin = Column(Boolean, default=False, nullable=False)

class AudioFile(Base):
    __tablename__ = "audio_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    path = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")
