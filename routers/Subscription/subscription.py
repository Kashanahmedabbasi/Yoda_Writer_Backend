from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from ..Subscription import crud, schemas
from ..Packages import crud as PkgCrud
import models
import datetime

router = APIRouter(
    prefix='/Subscription',
    tags=['Subscription'],
    responses={404: {"description": "Not found"}}
)


@router.post('/Create-Subscription')
async def createSubscription(data:schemas.CreateSubscription, db:Session = Depends(get_db)):
    try:
        return crud.createSubscription(data=data, db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.post('/Update-Order-Status')
async def updateOrderStatus(data:schemas.UpdateOrderStatus, db:Session = Depends(get_db)):
    try:
       return crud.updateOrderStatus(data=data, db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/Get-All-Pending-Orders')
async def getAllSubscriptions(db:Session = Depends(get_db)):
    try:
        Image_subscriptions = db.query(models.ImagePkgOrder).filter(models.ImagePkgOrder.Status=='pending').all()
        Write_subscriptions = db.query(models.WritePkgOrder).filter(models.WritePkgOrder.Status=='pending').all()
        return {'detail':{'ImagePackageOrders':Image_subscriptions,
                          'WritePackageOrders':Write_subscriptions},
                          'status_code':status.HTTP_200_OK}
    except:
        HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/Get-All-Active-Orders')
async def getAllSubscriptions(db:Session = Depends(get_db)):
    try:
        Image_subscriptions = db.query(models.ImagePkgOrder).filter(models.ImagePkgOrder.Status=='active').all()
        Write_subscriptions = db.query(models.WritePkgOrder).filter(models.WritePkgOrder.Status=='active').all()
        return {'detail':{'ImagePackageSubscriptions':Image_subscriptions,
                          'WritePackageSubscriptions':Write_subscriptions},
                          'status_code':status.HTTP_200_OK}
    except:
        HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/Get-All-Orders')
async def getAllSubscriptions(db:Session = Depends(get_db)):
    try:
        Image_subscriptions = db.query(models.ImagePkgOrder).all()
        Write_subscriptions = db.query(models.WritePkgOrder).all()
        return {'detail':{'ImagePackageSubscriptions':Image_subscriptions,
                          'WritePackageSubscriptions':Write_subscriptions},
                          'status_code':status.HTTP_200_OK}
    except:
        HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/Get-All-Pending-Subscriptions')
async def getAllSubscriptions(db:Session = Depends(get_db)):
    try:
        Image_subscriptions = db.query(models.ImagePkgSubscription).filter(models.ImagePkgSubscription.Status=='pending').all()
        Write_subscriptions = db.query(models.WritePkgSubscription).filter(models.WritePkgSubscription.Status=='pending').all()
        return {'detail':{'ImagePackageSubscriptions':Image_subscriptions,
                          'WritePackageSubscriptions':Write_subscriptions},
                          'status_code':status.HTTP_200_OK}
    except:
        HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/Get-All-Active-Subscriptions')
async def getAllSubscriptions(db:Session = Depends(get_db)):
    try:
        Image_subscriptions = db.query(models.ImagePkgSubscription).filter(models.ImagePkgSubscription.Status=='active').all()
        Write_subscriptions = db.query(models.WritePkgSubscription).filter(models.WritePkgSubscription.Status=='active').all()
        return {'detail':{'ImagePackageSubscriptions':Image_subscriptions,
                          'WritePackageSubscriptions':Write_subscriptions},
                          'status_code':status.HTTP_200_OK}
    except:
        HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@router.get('/Get-All-Subscriptions')
async def getAllSubscriptions(db:Session = Depends(get_db)):
    try:
        Image_subscriptions = db.query(models.ImagePkgSubscription).all()
        Write_subscriptions = db.query(models.WritePkgSubscription).all()
        return {'detail':{'ImagePackageSubscriptions':Image_subscriptions,
                          'WritePackageSubscriptions':Write_subscriptions},
                          'status_code':status.HTTP_200_OK}
    except:
        HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


