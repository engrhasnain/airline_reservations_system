from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )

    # SMTP / Email settings (optional)
    SMTP_HOST: str = os.getenv('SMTP_HOST')
    SMTP_PORT: str = os.getenv('SMTP_PORT')
    SMTP_USER: str = os.getenv('SMTP_USER')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')
    SMTP_USE_SSL: bool = os.getenv('SMTP_USE_SSL', '1') == '1'
    EMAIL_FROM: str = os.getenv('EMAIL_FROM', SMTP_USER)

settings = Settings()
