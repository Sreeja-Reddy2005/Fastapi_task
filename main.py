from fastapi import FastAPI
from models import Products

app = FastAPI()
@app.get("/")
def greeting():
    return "welcome sreeja"

product=[
    Products(id=1,name="phone",description="budget phone",price=99,quantity=2),
    Products(id=2,name="laptop",description="laptop",price=999,quantity=4),
    Products(id=3,name="airpods",description="wireless pods",price=89,quantity=6),
    Products(id=4,name="watch",description="smart watch",price=65,quantity=9),
]

@app.get("/products")
def get_all_products():
    return product

@app.get("/products/{id}")
def get_product_id(id:int):
    for item in product:
        if item.id == id:
            return item
    return "product not found"

@app.post("/products")
def add_the_products(new_product:Products):
    product.append(new_product)
    return new_product

@app.put("/products")
def update_the_product(id:int, update_product:Products):
    for i in range(len(product)):
        if product[i].id==id:
            product[i]=update_product
            return "products added sucessfully"
    return "no product found"

@app.delete("/products")
def delete_the_product(id:int):
    for i in range(len(product)):
        if product[i].id==id:
            del product[i]
            return "products deleted sucessfully"
    return "no product found"
