from fastapi import Header, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from routers.User import crud


async def get_current_user(token: Annotated[str, Header()], db: Session = Depends(get_db)):
    current_user = crud.get_current_user(token, db=db)
    if not current_user:
        raise HTTPException(status_code=400, detail="Could not validate User.")
