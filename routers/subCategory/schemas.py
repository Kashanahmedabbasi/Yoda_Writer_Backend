from pydantic import BaseModel

class AddSubCategory(BaseModel):
    CategoryName:str
    Name:str
    Summary:str
    Prompt:str
    Status:str

class UpdateSubCategory(AddSubCategory):
    SubCategoryId:int