from pydantic import BaseModel

class UserCreate(BaseModel):
    FirstName:str
    LastName:str
    Email:str
    Password:str
    Country:str
    Type:str

class UserLogin(BaseModel):
    Email:str
    Password:str

# class Token(BaseModel):
#     access_token:str
#     token_type:str    