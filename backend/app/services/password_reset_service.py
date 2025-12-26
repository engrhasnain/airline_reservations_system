from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import Session
from app.models.password_reset import PasswordReset


def create_reset_token(db: Session, email: str, minutes_valid: int = 30):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=minutes_valid)
    pr = PasswordReset(email=email, token=token, expires_at=expires_at)
    db.add(pr)
    db.commit()
    db.refresh(pr)
    return pr.token


def verify_reset_token(db: Session, email: str, token: str):
    pr = db.query(PasswordReset).filter(PasswordReset.email == email, PasswordReset.token == token).first()
    if not pr:
        return False
    if datetime.utcnow() > pr.expires_at:
        # expired: remove it
        db.delete(pr)
        db.commit()
        return False
    return True


def consume_reset_token(db: Session, token: str):
    pr = db.query(PasswordReset).filter(PasswordReset.token == token).first()
    if pr:
        db.delete(pr)
        db.commit()
