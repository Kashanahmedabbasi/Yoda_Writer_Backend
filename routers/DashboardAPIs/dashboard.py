from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
import models
from datetime import datetime, timedelta
from ..DashboardAPIs import crud

router = APIRouter(
    prefix='/Dashboard',
    tags=['Dashboard'],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)

@router.get('/Weekly-User-Registration')
async def weeklyRegistration(db :Session = Depends(get_db)):
    try:
        Users = db.query(models.User).all()
        start_of_week = crud.get_start_of_week()
        weekly_registrations = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
        total_registrations = 0
        for User in Users:
            registration_date = datetime.strptime(User.Date, "%d-%m-%Y")
            if start_of_week <= registration_date < start_of_week + timedelta(days=7):
                day_of_week = registration_date.strftime("%A") 
                weekly_registrations[day_of_week] += 1
                total_registrations += 1


        return {'detail': {'weekly_registrations':weekly_registrations,
                           'total_registrations':total_registrations},
                'status_code':status.HTTP_200_OK}

    except:
        HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/Show-Stats')
async def showStats(db:Session = Depends(get_db)):
    try:
        Users = db.query(models.User).filter(models.User.Status != 'pending').all()
        ImageSubscriptions = db.query(models.ImagePkgSubscription).filter(models.ImagePkgSubscription.Status != 'pending').all()
        WriteSubscriptions = db.query(models.WritePkgSubscription).filter(models.WritePkgSubscription.Status != 'pending').all()
        totalSubCategories = db.query(models.SubCategory).filter(models.SubCategory.Status != 'pending').all()

        return {'detail':{
            'TotalUsers':len(Users),
            'TotalSubCategories':len(totalSubCategories),
            'TotalSubscriptions':(len(ImageSubscriptions)+len(WriteSubscriptions))
        }, 'status_code':status.HTTP_200_OK}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)