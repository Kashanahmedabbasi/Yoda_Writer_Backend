from pydantic import BaseModel
from typing import Optional, List

class Package(BaseModel):
    
    Name:str
    SubCategoryName:str
    GeneratedCharacters:Optional[int] = None
    GeneratedImages:Optional[int] = None
    WriteLanguages:Optional[str] = None
    WriteTones:Optional[str] = None
    Status:str
    IsTrail:str
    MonthlyPrice:float
    YearlyPrice:float

class AddPackage(Package):
    Type:str

class UpdatePackage(AddPackage):
    PackageId:int    

    