from pydantic import BaseModel
from typing import Optional

class AddCategory(BaseModel):
    Name:str
    Status:str

# class UpdateCategory(BaseModel):
#     Name:Optional[str]
#     Status:Optional[str]