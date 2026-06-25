

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS512"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(username: str, fullName: str, email: str, userId: str):
    payload = {
        "sub": username,
        "fullNamae": fullName,
        "userId": userId,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")