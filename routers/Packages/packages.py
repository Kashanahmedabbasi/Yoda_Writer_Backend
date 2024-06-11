from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from ..Packages import schemas, crud
import models

router = APIRouter(
    prefix='/Packages',
    tags=['Packages'],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)


@router.post('/Add-Package')
async def addPackage(package:schemas.AddPackage = Depends(),db:Session = Depends(get_db)):
    try:
        return crud.addPackage(package=package, db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/Get-All-Packages')
async def getAllPackages(db:Session = Depends(get_db)):
    try:
        return crud.getAllPackages(db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put('/Update-Package')
async def updatePackage(data:schemas.UpdatePackage, db:Session=Depends(get_db)):
    try:
        return crud.updatePackage(data=data, db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)   

@router.delete('/Delete-Package')
async def deletePackage(PackageId:int, PackageType:str, db:Session = Depends(get_db)):
    try:
        return crud.deletePackage(PackageId=PackageId,PackageType=PackageType,db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 