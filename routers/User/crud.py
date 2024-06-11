from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import models
from ..User import schemas
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
import datetime
import os, dotenv

dotenv.load_dotenv('Yoda_Writer_Backend\.env\confidential.env')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SecretKey = os.getenv('JWT_SECRET_KEY')
Algorithm = os.getenv('ALGORITHM')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, Email: str):
    return db.query(models.User).filter(models.User.Email == Email).first()

def get_user_by_id(db:Session, UserId:int):
    return db.query(models.User).filter(models.User.Id == UserId).first()

def get_current_user(token:str,db: Session):
    try:
        payload = jwt.decode(token,SecretKey,algorithms=Algorithm)
        email : str = payload.get('Email')
        username : str = payload.get('UserName')
        id:int=payload.get('id')
        if username is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")
        
        user = get_user_by_email(db=db,Email=email)
        if user:
            return JSONResponse({
                'id':id,
                'UserName':username,
                'Email':email
            })
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")

def get_user(db: Session, Email:str, Password:str):
    getUser = db.query(models.User).filter(models.User.Email==Email).first()
    if getUser:
        if pwd_context.verify(Password, getUser.Password):
            return getUser
        else:
            return 'Incorrect Password Entered'
    else:
       return 'Incorrect Email Entered'

def createAccessToken(Email:str, UserName:str):
    encode = {'Email':Email, 'UserName':UserName}
    return jwt.encode(encode,SecretKey,algorithm=Algorithm)

def createUser(db:Session, user:schemas.UserCreate):
    today = datetime.date.today()
    todayDate = today.strftime("%d-%m-%Y")

    user = models.User(FirstName=user.FirstName, LastName=user.LastName, Email=user.Email, 
                       Password=pwd_context.hash(user.Password), Country=user.Country, Status = 'pending',
                       Type = user.Type, Date=todayDate)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user