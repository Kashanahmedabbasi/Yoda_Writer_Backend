from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from ..User import schemas, crud
import models



router = APIRouter(
    prefix='/User',
    tags=['User'],
    responses={404: {"description": "Not found"}},
)


@router.post('/SignUp')
async def signUp(user:schemas.UserCreate, db:Session=Depends(get_db)):
    try:
        checkUser = crud.get_user_by_email(db=db, Email=user.Email)
        if checkUser:
            return {'detail':'Email already Registered',
                    'status_code':status.HTTP_400_BAD_REQUEST}
        else:
            User = crud.createUser(db=db,user=user)
            UserName = User.FirstName+" "+User.LastName
            token = crud.createAccessToken(Email=User.Email, UserName=UserName)
            return JSONResponse({
                
                'detail':{
                'AccessToken':token,
                'UserId':User.Id,
                'UserEmail':User.Email
            }
            ,'status_code':status.HTTP_200_OK
            })

    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.post('/LogIn')
async def logIn(user:schemas.UserLogin, db:Session = Depends(get_db)):
    try:
        loginUser = crud.get_user(db=db, Email=user.Email, Password=user.Password)
        if isinstance(loginUser,models.User):
            UserName = loginUser.FirstName+" "+loginUser.LastName
            token = crud.createAccessToken(Email=loginUser.Email, UserName=UserName)
            return JSONResponse({'detail':{
                'AccessToken':token,
                'UserId':loginUser.Id,
                'UserEmail':loginUser.Email
            },
            'status_code':status.HTTP_200_OK})
        else:
            return {'detail':loginUser,
                    'status_code':status.HTTP_404_NOT_FOUND}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
@router.post('/Change-User-Status')
async def changeUserStatus(UserStatus:str, UserId:int, db:Session = Depends(get_db)):
    try:
        user = crud.get_user_by_id(db=db, UserId=UserId)
        if user:
            user.Status = UserStatus
            db.commit()
            db.refresh(user)
            return {'detail':'User status changed successfully',
                    'status_code':status.HTTP_200_OK}
        else:
            return {'detail':'User does not exist',
                    'status_code':status.HTTP_404_NOT_FOUND}    
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
