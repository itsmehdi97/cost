import os
from typing import List
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


from database import Session
import schemas
import crud
import utils
import config



app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()



async def get_current_user(
        db: Session=Depends(get_db),
        token: str=Depends(oauth2_scheme)
    ):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    settings = config.get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = utils.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/ping")
async def ping():
    return JSONResponse(status_code=204)


@app.post("/token/", response_model=schemas.Token)
def login(db: Session=Depends(get_db), form_data: OAuth2PasswordRequestForm=Depends()):

    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=config.get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username, "uid": user.id}, expires_delta=access_token_expires)
   
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    


@app.get("/me/", response_model=schemas.User)
def me(user: schemas.User=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    return user


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int=0, limit: int=50, db: Session=Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists.")

    return crud.create_user(db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user

