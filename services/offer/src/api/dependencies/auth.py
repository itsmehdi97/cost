from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import jwt_utils
from schemas.user import User
from core.config import get_settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def current_user(token: str = Depends(oauth2_scheme)):
    settings = get_settings()

    payload = jwt_utils.verify_token(token, settings.SECRET_KEY)
    if payload:
        return User(id=payload.get('uid'), username=payload.get('sub'))
    raise HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )