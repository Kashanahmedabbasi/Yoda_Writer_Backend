import math
from fastapi import HTTPException, status
import models, os
from ..Category import schemas
from sqlalchemy.orm import Session
from pathlib import Path


def upload_Icon_file(file,category:schemas.AddCategory):
    file_extension = file.filename.split(".")[-1]
    allowed_extensions = ["jpg", "jpeg", "png"]
    if file_extension.lower() not in allowed_extensions:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File Type Invalid")
    
    try:
        contents = file.file.read()
        parent_dir='Yoda_Writer_Backend/static/Category/Icons'
        category_path = f'{parent_dir}/{category.Name}'
        if Path(category_path).exists():
            file_path = f'{category_path}/{file.filename}'
            with open(file_path, 'wb') as f:
                f.write(contents)
                f.flush()
                f.close()
            return file_path
        else:
            Path(category_path).mkdir(parents=True)
            file_path = f'{category_path}/{file.filename}'
            with open(file_path, 'wb') as f:
                f.write(contents)
                f.flush()
                f.close()
            return file_path

    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error Uploading File")


def getCategoryByName(Name:str, db:Session):
    return db.query(models.Category).filter(models.Category.Name==Name).first()

def getCategoryById_Values(Id:int, db:Session):
    return db.query(models.Category).filter(models.Category.Id==Id).first()

def getCategoryById(Id:int, db:Session):
    return db.query(models.Category).filter(models.Category.Id==Id)

def change_category_folder_name(old_name:str, new_name:str):
    #_____________________Renaming Directory according to new Category Name___________________________________*
    path = 'Yoda_Writer_Backend/static/Category/Icons'
    try:
        for root, dirs, files in os.walk(path):
            for dir_name in dirs:
                if dir_name == old_name:
                    old_path = os.path.join(root, dir_name)
                    new_path = os.path.join(root, new_name)

                    os.rename(old_path, new_path)
                    return Path(new_path)
    except Exception as e:
        print(f"An error occurred: {e}")

def save_Icon_logo_file(new_path:str, file):  
     #_____________________Saving New Icon File to Renamed Folder___________________________________*
    file_extension = file.filename.split(".")[-1]
    allowed_extensions = ["jpg", "jpeg", "png"]
    if file_extension.lower() not in allowed_extensions:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File Type Invalid") 
    try:
        contents = file.file.read()
        file_path = f'{new_path}/{file.filename}'
        with open(file_path, 'wb') as f:
            f.write(contents)
            f.close()
        return file_path
    except:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something Went Wrong")
    

def deleteCategory(CategoryId:int, db:Session):
    CategoryValues = getCategoryById_Values(Id=CategoryId, db=db)
    db.query(models.SubCategory).filter(models.SubCategory.CategoryId==CategoryId).delete(synchronize_session=False)
    Category = getCategoryById(Id=CategoryId, db=db).delete(synchronize_session=False)
    file_path = CategoryValues.Icon

    # Split the file path
    directory_path, file_name = os.path.split(file_path)

    # Remove Category Icon File
    try:
        os.remove(file_path)
    except FileNotFoundError:
        return (f"File '{file_path}' not found.")
    
    # Removing Category Directory
    try:
        os.rmdir(directory_path)
    except FileNotFoundError:
        return (f"Parent directory '{directory_path}' not found.")
    
    db.commit()
    return {'detail':'Category removed successfully',
            'status_code':status.HTTP_200_OK}

def getCategoryByPageNo(PageNo:int, Limit:int, db:Session):
    end_index = PageNo*Limit
    start_index = (end_index-Limit)
    total_rows = db.query(models.Category).count()
    total_pages = (total_rows / Limit)
    if total_pages % 1 > 0:
        # Round up to the next whole number
        total_pages_rounded = math.ceil(total_pages)
    else:
        # It's already a whole number
        total_pages_rounded = int(total_pages)

    Pages=list(range(1, int(total_pages)+1 ))
    if (end_index>total_rows):
        end_index=total_rows
    if(start_index>end_index):
        return HTTPException(detail='Page Does Not Exist', status_code=status.HTTP_404_NOT_FOUND)    
    Categories=[]
    categories = db.query(models.Category).order_by(models.Category.Id.desc()).slice(start=start_index, stop=end_index).all()
    for category in categories:
        Categories.append(category)      
    return {'detail':{'PageNo':PageNo,
            'Data':Categories,
            'TotalPages':total_pages_rounded,
            'TotalCategories':total_rows},
            'status_code':status.HTTP_200_OK
            }  
