import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default for local dev
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")  # Use a secure value in production
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # Yandex OAuth Config
    YANDEX_AUTH_URL: str = "https://oauth.yandex.ru/authorize"
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"
    YANDEX_USER_INFO_URL: str = "https://login.yandex.ru/info"
    YANDEX_CLIENT_ID: str = os.getenv("YANDEX_CLIENT_ID", "default_client_id")
    YANDEX_CLIENT_SECRET: str = os.getenv("YANDEX_CLIENT_SECRET", "default_client_secret")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/yandex")

    def __init__(self):
        # Ensure essential environment variables are set
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set")
        if not self.SECRET_KEY or self.SECRET_KEY == "your_secret_key":
            raise ValueError("SECRET_KEY is not set or using the default value, please set a secure secret key.")
        if not self.YANDEX_CLIENT_ID or self.YANDEX_CLIENT_ID == "default_client_id":
            raise ValueError("YANDEX_CLIENT_ID is not set or using the default value, please set a valid client ID.")
        if not self.YANDEX_CLIENT_SECRET or self.YANDEX_CLIENT_SECRET == "default_client_secret":
            raise ValueError("YANDEX_CLIENT_SECRET is not set or using the default value, please set a valid client secret.")


settings = Settings()

