from pydantic import BaseModel

class CreateSubscription(BaseModel):
    PackageName:str
    PackageType:str
    UserId:int

class UpdateOrderStatus(BaseModel):
    OrderId:int
    OrderType:str
    Amount:float
    TransactionId:str

