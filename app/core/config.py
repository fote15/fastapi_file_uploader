import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    YANDEX_AUTH_URL: str = "https://oauth.yandex.ru/authorize"
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"
    YANDEX_USER_INFO_URL: str = "https://login.yandex.ru/info"
    YANDEX_CLIENT_ID: str = "9795c01634bb487e96edbca33d6525f6"
    YANDEX_CLIENT_SECRET: str = "52e579a83a1347d18f0d5da439caaa14"
    REDIRECT_URI: str = "http://localhost:8000/auth/yandex"

settings = Settings()

