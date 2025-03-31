from fastapi import FastAPI
from app.api.routes import auth, users, files
from app.core.config import settings

app = FastAPI(title="Audio File Service", version="1.0.0")

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(files.router, prefix="/files", tags=["Files"])
