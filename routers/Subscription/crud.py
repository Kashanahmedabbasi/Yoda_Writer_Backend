from fastapi import status
from sqlalchemy.orm import Session
from ..Subscription import schemas
from ..Packages import crud as PkgCrud
import models
import datetime



def createSubscription(data:schemas.CreateSubscription, db:Session):
    package = PkgCrud.getPackageByName(PackageName=data.PackageName, PackageType=data.PackageType, db=db)
    if type(package) in (models.WritePackages , models.ImagePackages):
        if type(package) is (models.WritePackages):
            subscription = models.WritePkgSubscription(PackageId=package.Id, UserId=data.UserId, Status='pending',
                                                        TotalCharacters=package.GeneratedCharacters, RemainingCharacters=package.GeneratedCharacters)
            db.add(subscription)
            db.commit()
            order = models.WritePkgOrder(SubscriptionId=subscription.Id, Amount=0.0, TransactionId='-', Status=subscription.Status,
                                        StartDate='-', EndDate='-' )
            db.add(order)
            db.commit()
            
            return {'detail':'Subscription Added Successfully',
                    'status_code':status.HTTP_200_OK}
        elif type(package) is (models.ImagePackages):
            subscription = models.ImagePkgSubscription(PackageId=package.Id, UserId=data.UserId, Status='pending',
                                                        TotalImages=package.GeneratedImages, RemainingImages=package.GeneratedImages)
            db.add(subscription)
            db.commit()
            order = models.ImagePkgOrder(SubscriptionId=subscription.Id, Amount=0.0, TransactionId='-', Status=subscription.Status,
                                        StartDate='-', EndDate='-' )
            db.add(order)
            db.commit()
            return {'detail':'Subscription Added Successfully',
                    'status_code':status.HTTP_200_OK}
        
    elif type(package) is dict:
        return package
    else:
        return {'detail':'Package does not exist',
                'status_code':status.HTTP_404_NOT_FOUND}
    

def updateOrderStatus(data:schemas.UpdateOrderStatus, db:Session):
    today = datetime.date.today()
    one_month_later = today + datetime.timedelta(days=30)
    today_date = today.strftime("%d-%m-%Y")
    one_month_later_date = one_month_later.strftime("%d-%m-%Y")
    if (data.OrderType=='write'):
        order = db.query(models.WritePkgOrder).filter(models.WritePkgOrder.Id==data.OrderId)
        orderData = db.query(models.WritePkgOrder).filter(models.WritePkgOrder.Id==data.OrderId).first()
        updatedData = {
            'SubscriptionId':orderData.SubscriptionId,
            'Amount':data.Amount,
            'TransactionId':data.TransactionId,
            'Status':'active',
            'StartDate':today_date,
            'EndDate':one_month_later_date
        }
        subscription = db.query(models.WritePkgSubscription).filter(models.WritePkgSubscription.Id==orderData.SubscriptionId).first()
        subscription.Status='active'
        order.update(updatedData)
        db.commit()
        return {'detail':'Order Activated',
                'status_code':status.HTTP_200_OK}

    elif(data.OrderType=='image'):
        order = db.query(models.ImagePkgOrder).filter(models.ImagePkgOrder.Id==data.OrderId)
        orderData = db.query(models.ImagePkgOrder).filter(models.ImagePkgOrder.Id==data.OrderId).first()
        updatedData = {
            'SubscriptionId':orderData.SubscriptionId,
            'Amount':data.Amount,
            'TransactionId':data.TransactionId,
            'Status':'active',
            'StartDate':today_date,
            'EndDate':one_month_later_date
        }
        subscription = db.query(models.ImagePkgSubscription).filter(models.ImagePkgSubscription.Id==orderData.SubscriptionId).first()
        subscription.Status='active'
        order.update(updatedData)
        db.commit()
        return {'detail':'Order Activated',
                'status_code':status.HTTP_200_OK}
    else:
        return {'detail':'Invalid Order Type Provided',
                'status_code':status.HTTP_406_NOT_ACCEPTABLE}