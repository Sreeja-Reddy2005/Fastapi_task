from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Float,Boolean
Base=declarative_base()



class Products(Base):
    __tablename__="product"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity =  Column(Integer)

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    user_name=Column(String(255),unique=True,index=True)
    email=Column(String(255),unique=True,index=True)
    hashed_password=Column(String(255))
    role=Column(String(50),default="user")
    is_active = Column(Boolean, default=True)
