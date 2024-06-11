from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..Packages import schemas
from ..SubCategory import crud as SubCategoryCRUD
import models
from typing import List

def getPackageByIdOBJ(PackageId:int, PackageType:str, db:Session):
    if PackageType.lower()=='write':
        return db.query(models.WritePackages).filter(models.WritePackages.Id==PackageId)
    elif PackageType.lower()=='image':
        return db.query(models.ImagePackages).filter(models.ImagePackages.Id==PackageId)

def getPackageById(PackageId:int, PackageType:str, db:Session):
    if PackageType.lower()=='write':
        return db.query(models.WritePackages).filter(models.WritePackages.Id==PackageId).first()
    elif PackageType.lower()=='image':
        return db.query(models.ImagePackages).filter(models.ImagePackages.Id==PackageId).first()
    else:
        return '#'  
      
def getPackageByName(PackageName:str, PackageType:str, db:Session):
    if PackageType.lower()=='write':
        return db.query(models.WritePackages).filter(models.WritePackages.Name==PackageName).first()
    elif PackageType.lower()=='image':
        return db.query(models.ImagePackages).filter(models.ImagePackages.Name==PackageName).first()
    else:
        return {'Detail':'Invalid Package Type'}    

def checkPackageName(Name:str, SubCategoryId:int, Type:str, db:Session):
    if Type.lower()=='write':
        return db.query(models.WritePackages).filter(models.WritePackages.SubCategoryId==SubCategoryId,
                                                     models.WritePackages.Name==Name).first()
    elif Type.lower()=='image':
        return db.query(models.ImagePackages).filter(models.ImagePackages.SubCategoryId==SubCategoryId,
                                                     models.ImagePackages.Name==Name).first()
    else:
        return "#"
    

def addPackage(package:schemas.AddPackage, db:Session):
    RegisteredPackages : List[str] = []
    SubCategoryNameList = package.SubCategoryName.split(',')
    for subCategory in SubCategoryNameList:
        subCategoryObj = SubCategoryCRUD.getSubCategoryByName(Name=subCategory ,db=db)
        checkPackage = checkPackageName(Name=package.Name, SubCategoryId=subCategoryObj.Id, Type=package.Type, db=db)
        if not checkPackage:
            # if type(checkPackage) in (models.WritePackages , models.ImagePackages):
                if package.Type.lower()=='write':
                    LanguagesList = package.WriteLanguages.split(',')
                    TonesList = package.WriteTones.split(',')
                    for Language in LanguagesList:
                        for Tone in TonesList:
                            data = models.WritePackages(
                                Name=package.Name,
                                GeneratedCharacters=package.GeneratedCharacters,
                                SubCategoryId=subCategoryObj.Id,
                                WriteLanguage=Language,
                                WriteTone=Tone,
                                Status=package.Status,
                                IsTrail=package.IsTrail,
                                MonthlyPrice=package.MonthlyPrice,
                                YearlyPrice=package.YearlyPrice
                            )
                            db.add(data)
                            db.commit()
                            db.refresh(data)
                elif package.Type.lower()=='image':
                    data = models.ImagePackages(
                        Name=package.Name,
                        GeneratedImages=package.GeneratedImages,
                        SubCategoryId=subCategoryObj.Id,
                        Status=package.Status,
                        IsTrail=package.IsTrail,
                        MonthlyPrice=package.MonthlyPrice,
                        YearlyPrice=package.YearlyPrice
                    )
                    db.add(data)
                    db.commit()
                    db.refresh(data)
            # else: 
            #     return {'Detail':'Invalid Package Type Provided'}
        else:
            if type(checkPackage) in (models.WritePackages , models.ImagePackages):
                RegisteredPackages.append(checkPackage)
            else:
                return {'detail':'Invalid Package Type Provided',
                        'status_code':status.HTTP_406_NOT_ACCEPTABLE}
    
    if len(RegisteredPackages)==0:
        return {'detail':'All Packages Added Successfully',
                'status_code':status.HTTP_200_OK}
    else:
        return {'detail':{'Message':'Some Packages are Already Registered',
                'Data':RegisteredPackages},
                'status_code':status.HTTP_200_OK}
    

def updatePackage(data:schemas.UpdatePackage, db:Session):
    getPackage = getPackageById(PackageId=data.PackageId, PackageType=data.Type, db=db)
    if getPackage and type(getPackage) in (models.WritePackages , models.ImagePackages):
        subCategoryObj = SubCategoryCRUD.getSubCategoryByName(Name=data.SubCategoryName, db=db)
        if data.Type.lower()=='write':
            existingPackage = db.query(models.WritePackages).filter(models.WritePackages.Id==data.PackageId)
            updatedData = {
                'Name':data.Name,
                'GeneratedCharacters':data.GeneratedCharacters,
                'SubCategoryId':subCategoryObj.Id,
                'WriteLanguage':data.WriteLanguages,
                'WriteTone':data.WriteTones,
                'Status':data.Status,
                'IsTrail':data.IsTrail ,
                'MonthlyPrice':data.MonthlyPrice ,
                'YearlyPrice':data.YearlyPrice 
            }
            existingPackage.update(updatedData)
            db.commit()
            return {'Detail':'Package Updated Successfully'}
        elif data.Type.lower()=='image':
            existingPackage = db.query(models.ImagePackages).filter(models.ImagePackages.Id==data.PackageId)
            updatedData = {
                'Name':data.Name,
                'GeneratedImages':data.GeneratedImages,
                'SubCategoryId':subCategoryObj.Id,
                'Status':data.Status,
                'IsTrail':data.IsTrail ,
                'MonthlyPrice':data.MonthlyPrice ,
                'YearlyPrice':data.YearlyPrice 
            }
            existingPackage.update(updatedData)
            db.commit()
            return {'detail':'Package Updated Successfully',
                    'status_code':status.HTTP_200_OK}
    elif getPackage and type(getPackage) is str:
        return {'detail':'Invalid Package Type Provided',
                'status_code':status.HTTP_406_NOT_ACCEPTABLE}   
    else:
        return {'detail':'Package does not exist',
                'status_code':status.HTTP_404_NOT_FOUND}    
    
def deletePackage(PackageId:int,PackageType:str, db:Session):
    checkPackage = getPackageById(PackageId=PackageId, PackageType=PackageType, db=db)
    if checkPackage and type(checkPackage) in (models.WritePackages , models.ImagePackages):
        if PackageType.lower()=='write' or PackageType.lower()=='image':
            package = getPackageByIdOBJ(PackageId=PackageId, PackageType=PackageType, db=db)
            package.delete(synchronize_session=False)
            db.commit()
            return {'detail':'Package successfully deleted',
                    'status_code':status.HTTP_200_OK}
        else:
            return {'detail':'Invalid Package Type Provided',
                    'status_code':status.HTTP_406_NOT_ACCEPTABLE}
    else:
        return {'detail':'Package does not exist',
                'status_code':status.HTTP_404_NOT_FOUND}
    

def getAllPackages(db:Session):
    writePackages = db.query(models.WritePackages).all()
    imagePackages = db.query(models.ImagePackages).all()
    return{'detail':{'WritePackages':writePackages,
           'ImagePackages':imagePackages},
           'status_code':status.HTTP_200_OK}