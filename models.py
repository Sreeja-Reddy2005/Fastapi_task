from pydantic import BaseModel,Field,EmailStr

class Usercreate(BaseModel):
    username:str
    email:str
    password:str = Field(...,min_length=6,max_length=15)

class UserLogin(BaseModel):
    username:str
    password:str = Field(...,min_length=6,max_length=15)



class Products(BaseModel):
    id : int
    name: str = Field(...,min_length=1)
    description:str
    price:float = Field(...,gt=0)
    quantity: int = Field(...,ge=0)
    
    class Config:
        from_attributes = True


