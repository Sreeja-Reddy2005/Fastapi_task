from pydantic import BaseModel,Field

class Products(BaseModel):
    id : int
    name: str = Field(...,min_length=1)
    description:str
    price:float = Field(...,gt=0)
    quantity: int = Field(...,ge=0)
    
    class Config:
        from_attributes = True


