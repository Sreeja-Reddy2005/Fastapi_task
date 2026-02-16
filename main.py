from fastapi import Depends,FastAPI
from models import Products
from fastapi import HTTPException
from database import session,engine
import database_models

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
