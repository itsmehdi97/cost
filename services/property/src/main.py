from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import crud
import schemas
from database import Session
import jwt_utils


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# TODO:
SECRET = "SECRET_KEY"

async def current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt_utils.verify_token(token, SECRET)
    if payload:
        return schemas.User(id=payload.get('uid'), username=payload.get('sub'))
    raise HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.post("/properties/", response_model=schemas.Property)
async def create_property(
        property: schemas.PropertyCreate,
        db: Session = Depends(get_db),
        user: schemas.User = Depends(current_user)
    ):
    db_prop = crud.get_property(db, user.id, property.title)
    if db_prop:
        raise HTTPException(
            status_code=400,
            detail="property already exists",
        )

    property.user_id = user.id
    return crud.create_property(db, property)


@app.put("/properties/{prop_id}", response_model=schemas.Property)
async def transfer_ownership(
        prop_id: int,
        prop: schemas.PropertyUpdate,
        user: schemas.User = Depends(current_user),
        db: Session = Depends(get_db)
    ):
        db_prop = crud.get_property_by_id(db, prop_id)
        if not db_prop:
            raise HTTPException(
                status_code=404,
                detail="Property not found"
            )
        
        if not db_prop.user_id == user.id:
            raise HTTPException(
                status_code=403,
                detail="Not allowed to update this property"
            )
        
        crud.update_property(db, prop)
        return db_prop
