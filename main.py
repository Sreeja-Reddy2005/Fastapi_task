from fastapi import Depends,FastAPI
from models import Products,UserLogin,Usercreate
from utils import hash_password,verify_password
from fastapi import HTTPException
from database import session,engine
import database_models
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer




app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greeting():
    return "welcome sreeja"



product=[
    Products(id=1,name="phone",description="budget phone",price=99,quantity=2),
    Products(id=2,name="laptop",description="laptop",price=999,quantity=4),
    Products(id=3,name="airpods",description="wireless pods",price=89,quantity=6),
    Products(id=4,name="watch",description="smart watch",price=65,quantity=9),
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db=session()
    count= db.query(database_models.Products).count()
    if count == 0:
        for products in product:
            db.add(database_models.Products(**products.model_dump()))
        db.commit()
init_db()

@app.get("/products")
def get_all_products(db:session = Depends(get_db)):
    db_products = db.query(database_models.Products).all()
    return db_products

@app.get("/products/{id}")
def get_product_id(id:int,db:session = Depends(get_db)):
    db_product=db.query(database_models.Products).filter(database_models.Products.id==id).first()
    
    if not db_product:
        raise HTTPException(status_code=404,detail = "product not found")
    return db_product

@app.post("/products")
def add_the_products(new_product: Products, db = Depends(get_db)):

    db_product = database_models.Products(**new_product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

    

@app.put("/products/{id}")
def update_the_product(id:int, update_product:Products,db:session=Depends(get_db)):
    db_product=db.query(database_models.Products).filter(database_models.Products.id==id).first()
    if db_product:
        db_product.name=update_product.name
        db_product.price=update_product.price
        db_product.description=update_product.description
        db_product.quantity=update_product.quantity
        db.commit()
        return "product_updated"
    raise HTTPException(status_code=404, detail="Product not found")
    

@app.delete("/products/{id}")
def delete_product(id:int,db:session=Depends(get_db)):
    db_product=db.query(database_models.Products).filter(database_models.Products.id==id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


SECRET_KEY="J_C868DAM0XIgUHnc8Xgxww6jANAv5TZAH2hEP_43cU"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 30


@app.post("/register")
def register(user:Usercreate,db=Depends(get_db)):
    existing_user = db.query(database_models.User).filter(
        database_models.User.email== user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already existed")
    
    hash_pwd = hash_password(user.password)

    new_user=database_models.User(
        user_name=user.username,
        email=user.email,
        hashed_password=hash_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"user registerd"}

@app.post("/login")
def login(user:UserLogin,db=Depends(get_db)):
    db_user=db.query(database_models.User).filter(
        database_models.User.user_name == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400,detail="user not found")
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=400,detail="Invalid password")
    access_token=create_access_token({'sub':db_user.user_name})
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
    

def create_access_token(data:dict):
    to_encode=data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


    
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = db.query(database_models.User).filter(
        database_models.User.user_name == username).first()
    if user is None:
        raise credential_exception
    if not user.is_active:
        raise HTTPException(status_code=400,detail="Inactive user")
    return user


@app.get("/profile")
def profile(current_user = Depends(get_current_user)):
    return {
        "username": current_user.user_name,
        "email": current_user.email,
        "role": current_user.role
    }




