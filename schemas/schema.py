from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional

ShopName='Bolt'

class Item(BaseModel):
    item_id: int = Field(...)
    name: str = Field(...,min_length=1)
    brand: str  = Field(...,min_length=1)
    price: float
    quantity: int


    @field_validator("item_id","quantity","price")
    def pos_num(cls,v,info):
        if v < 0:
            raise ValueError(f"Field {info.field_name} musn't be negative number")
        return v


class UpdateItem(BaseModel):
    item_id: Optional[int] = None 
    name: Optional[str] = None 
    brand: Optional[str] = None 
    price: Optional[float] = None 
    quantity: Optional[int] = None

    @field_validator("item_id","quantity","price")
    def pos_num(cls,v,info):
        if v is None:
            return v
        if v < 0:
            raise ValueError(f"Field {info.field_name} musn't be negative number")
        return v
class Basket(BaseModel):
    id: int
    user_id: int 
    items: List[Item]


    @field_validator("id","user_id")
    def pos_num(cls,v,info):
        if v < 0:
            raise ValueError(f"Field {info.field_name} musn't be negative number")
        return v

class User(BaseModel):
    id: int
    name: str = Field(...,min_length=1)
    email: EmailStr    


    @field_validator("id")
    def pos_num(cls,v,info):
        if v < 0:
            raise ValueError(f"Field {info.field_name} musn't be negative number")
        return v
    
    