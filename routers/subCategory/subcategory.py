from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from ..SubCategory import schemas, crud
from ..Category import crud as categoryCrud
from sqlalchemy.orm import Session
from dependencies import get_current_user
from typing import Optional
import models
from database import get_db
import os

router = APIRouter(
    prefix='/SubCategory',
    tags=['SubCategory'],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)


@router.post('/Add-SubCategory')
async def addSubCategory(subCategory:schemas.AddSubCategory= Depends(),file:UploadFile = File(...), db:Session = Depends(get_db)):
    try:
        checkCategory = categoryCrud.getCategoryByName(Name=subCategory.CategoryName, db=db)
        if checkCategory:
            checkSubCategory = crud.getSubCategoryByName(Name=subCategory.Name, db=db)
            if not checkSubCategory:
                Icon = crud.upload_Icon_file(file=file, SubCategory=subCategory)
                if type(Icon) is str:
                    SubCategory = models.SubCategory(CategoryId=checkCategory.Id,Name=subCategory.Name,
                                                     Summary=subCategory.Summary, Icon=Icon,Prompt=subCategory.Prompt, Status=subCategory.Status)
                    db.add(SubCategory)
                    db.commit()
                    db.refresh(SubCategory)
                    return {'detail':{'Message':'Category added Successfully',
                                      'Data':{
                                          'SubCategoryName':SubCategory.Name,
                                          'SubcategoryId':SubCategory.Id
                                      }},
                                      'status_code':status.HTTP_200_OK}
                else:
                    return Icon
            
            else:
                return {'detail':'SubCategory Already Exists',
                        'status_code':status.HTTP_406_NOT_ACCEPTABLE}
        else:
            return {'detail':'Category does not exist. Please select SubCategory for a category that exists.',
                    'status_code':status.HTTP_404_NOT_FOUND}
            
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/Get-SubCategories-By-Page-No')
async def getSubCategoriesByPageNo(PageNo:int, Limit:int, db:Session = Depends(get_db)):
    try:
        return crud.getSubCategoryByPageNo(PageNo=PageNo, Limit=Limit, db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  

@router.get('/Get-All-SubCategories')  
async def getAllSubCategories(db:Session = Depends (get_db)):
    try:
        categories = db.query(models.SubCategory).all()
        return {'detail':categories,
                'status_code':status.HTTP_200_OK}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

@router.put('/Update-SubCategory')
async def UpdateSubCategory(updateData:schemas.UpdateSubCategory = Depends(), file:Optional[UploadFile]=None, db:Session = Depends(get_db)):
    try:
        existingSubCategoryValues = crud.getSubCategoryById_Values(Id=updateData.SubCategoryId, db=db)
        if existingSubCategoryValues:
            checkCategory = categoryCrud.getCategoryByName(Name=updateData.CategoryName, db=db)
            if checkCategory:
                if file is None:
                    existingSubcategory = crud.getSubCategoryById(Id=updateData.SubCategoryId, db=db)
                    newSubCategoryDir = crud.change_SubCategory_folder_name(old_name=existingSubCategoryValues.Name, new_name=updateData.Name)
                    icon_file_name = os.path.basename(existingSubCategoryValues.Icon)
                    Icon = f'{newSubCategoryDir}/{icon_file_name}'
                    updatedSubCategory = {
                    'CategoryId':checkCategory.Id,   
                    'Name': updateData.Name,
                    'Summary':updateData.Summary,
                    'Icon': Icon.replace('\\','/'),
                    'Prompt':updateData.Prompt,
                    'Status': updateData.Status
                                        }
                    existingSubcategory.update(updatedSubCategory)
                    db.commit()
                    return {'detail':'SubCategory updated successfully',
                            'status_code':status.HTTP_200_OK}
                else:
                    existingSubcategory = crud.getSubCategoryById(Id=updateData.SubCategoryId, db=db)
                    newSubCategoryDir = crud.change_SubCategory_folder_name(old_name=existingSubCategoryValues.Name, new_name=updateData.Name)
                    Icon = crud.save_Icon_logo_file(new_path=newSubCategoryDir,file=file)
                    updatedSubCategory = {
                    'CategoryId':checkCategory.Id,   
                    'Name': updateData.Name,
                    'Summary':updateData.Summary,
                    'Icon': Icon.replace('\\','/'),
                    'Prompt':updateData.Prompt,
                    'Status': updateData.Status
                                        }
                    oldIcon = existingSubCategoryValues.Icon
                    existingSubcategory.update(updatedSubCategory)
                    db.commit()
                    os.remove(oldIcon)
                    return {'detail':'SubCategory updated successfully',
                            'status_code':status.HTTP_200_OK}
                    

            else:
                return {'detail':'Category does not exist. Please select Category for  SubCategory that exists.',
                        'status_code':status.HTTP_404_NOT_FOUND}

        else:
            return {'detail':'SubCategory does not exist',
                    'status_code':status.HTTP_404_NOT_FOUND}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/Delete-SubCategory')
async def deleteCategory(SubCategoryId:int, db:Session = Depends(get_db)):
    try:
        return crud.deleteSubCategory(SubCategoryId=SubCategoryId, db=db)

    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)