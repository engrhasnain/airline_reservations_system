from datetime import datetime, timedelta
import random

# Simple in-memory OTP store: {email: (code, expires_at)}
_OTPS = {}

def create_otp(email: str, minutes_valid: int = 5):
    code = f"{random.randint(0, 999999):06d}"
    expires_at = datetime.utcnow() + timedelta(minutes=minutes_valid)
    _OTPS[email] = (code, expires_at)
    return code

def verify_otp(email: str, code: str):
    tup = _OTPS.get(email)
    if not tup:
        return False
    stored_code, expires_at = tup
    if datetime.utcnow() > expires_at:
        del _OTPS[email]
        return False
    if stored_code == code:
        del _OTPS[email]
        return True
    return False

def clear_otp(email: str):
    _OTPS.pop(email, None)