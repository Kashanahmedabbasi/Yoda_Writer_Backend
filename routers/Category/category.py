from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from ..Category import schemas, crud
import models
import os

router = APIRouter(
    prefix='/Category',
    tags=['Category'],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)


@router.post('/Add-Category')
async def addCategory(category:schemas.AddCategory = Depends(),file:UploadFile = File(...), db:Session = Depends(get_db)):
    try:
        checkCategory = crud.getCategoryByName(Name=category.Name, db=db)
        if not checkCategory:
            Icon = crud.upload_Icon_file(file=file, category=category)
            if type (Icon) is str:
                Category = models.Category(Name=category.Name, Icon=Icon, Status=category.Status)
                db.add(Category)
                db.commit()
                db.refresh(Category)
                return {'detail':{'Message':'Category added Successfully',
                                  'Data':{'CategoryId':Category.Id,
                                          'CategoryName':Category.Name}},
                                          'status_code':status.HTTP_200_OK}
            else:
                 return Icon
        else:
            return {'detail':'Category with this Name already exists',
                    'status_code':status.HTTP_406_NOT_ACCEPTABLE}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get('/Get-categories-By-Page-No')
async def getCategoriesByPageNo(PageNo:int, Limit:int, db:Session = Depends(get_db)):
    try:
        return crud.getCategoryByPageNo(PageNo=PageNo, Limit=Limit, db=db)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
@router.get('/Get-All-Categories')
async def getAllCategories(db:Session = Depends (get_db)):
    try:
        categories = db.query(models.Category).all()
        return {'detail':categories,
                'status_code':status.HTTP_200_OK}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put('/Update-Category')
async def updateCategory(CategoryId:int,category:schemas.AddCategory = Depends(), file:Optional[UploadFile]=None, db:Session = Depends(get_db)):
    try:
        existingCategoryValues = crud.getCategoryById_Values(Id=CategoryId, db=db)
        if existingCategoryValues:
            if file is None:
                existingCategory = crud.getCategoryById(Id=CategoryId, db=db)
                newCategoryDir = crud.change_category_folder_name(old_name=existingCategoryValues.Name, new_name=category.Name)
                icon_file_name = os.path.basename(existingCategoryValues.Icon)
                Icon = f'{newCategoryDir}/{icon_file_name}'
                updatedCategory = {
                    'Name': category.Name,
                    'Icon': Icon.replace('\\','/'),
                    'Status': category.Status
                }
                existingCategory.update(updatedCategory)
                db.commit()
                return {'detail':'Category updated successfully',
                        'status_code':status.HTTP_200_OK}
            else:
                existingCategory = crud.getCategoryById(Id=CategoryId, db=db)
                newCategoryDir = crud.change_category_folder_name(old_name=existingCategoryValues.Name, new_name=category.Name)
                Icon = crud.save_Icon_logo_file(new_path=newCategoryDir,file=file)
                updatedCategory = {
                    'Name': category.Name,
                    'Icon': Icon.replace('\\','/'),
                    'Status': category.Status
                }
                oldIcon=existingCategoryValues.Icon
                existingCategory.update(updatedCategory)
                db.commit()
                os.remove(oldIcon)
                return {'detail':'Category updated successfully',
                        'status_code':status.HTTP_200_OK}
                
        else:
            return {'detail':'Category does not exist',
                    'status_code':status.HTTP_404_NOT_FOUND}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.delete('/Delete-Category')
async def deleteCategory(CategoryId:int, db:Session = Depends(get_db)):
    try:
        return crud.deleteCategory(CategoryId=CategoryId, db=db)

    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)