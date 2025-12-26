from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, Token, ForgotRequest, ResetRequest
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.config import settings
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return create_user(db, user)

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate OTP and send via email
    from app.services.otp_service import create_otp
    from app.services.email_service import send_email

    code = create_otp(user.email)
    body = f"Your login code is: {code}. It expires in 5 minutes."
    try:
        send_email(user.email, "Your login code", body)
    except Exception:
        pass

    return {"detail": "otp_sent"}


from pydantic import BaseModel
class VerifyRequest(BaseModel):
    email: str
    code: str

@router.post("/verify", response_model=Token)
def verify_otp_route(data: VerifyRequest, db: Session = Depends(get_db)):
    from app.services.otp_service import verify_otp
    from app.services.email_service import send_email

    ok = verify_otp(data.email, data.code)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token({
        "sub": user.email,
        "is_admin": user.is_admin
    })

    # optional: send notification that login was successful
    try:
        send_email(user.email, "Login successful", "You have successfully logged in to Airline Reservation System.")
    except Exception:
        pass

    return {"access_token": token}


@router.post('/forgot')
def forgot_password(data: ForgotRequest, db: Session = Depends(get_db)):
    from app.services.password_reset_service import create_reset_token
    from app.services.email_service import send_email

    user = get_user_by_email(db, data.email)
    # Do not reveal whether the email exists
    if not user:
        return {"detail": "reset_sent"}

    token = create_reset_token(db, user.email)
    frontend = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    link = f"{frontend}/reset-password?email={user.email}&token={token}"
    body = f"To reset your password, click the link below (valid for 30 minutes):\n\n{link}"
    try:
        send_email(user.email, "Password reset", body)
    except Exception:
        pass

    return {"detail": "reset_sent"}


@router.post('/reset')
def reset_password(data: ResetRequest, db: Session = Depends(get_db)):
    from app.services.password_reset_service import verify_reset_token, consume_reset_token
    from app.core.security import hash_password
    from app.services.email_service import send_email

    ok = verify_reset_token(db, data.email, data.token)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(data.new_password)
    db.commit()

    # consume token
    consume_reset_token(db, data.token)

    try:
        send_email(user.email, "Password changed", "Your account password has been changed successfully.")
    except Exception:
        pass

    return {"detail": "password_reset"}
