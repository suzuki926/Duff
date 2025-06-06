from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from .models import Product
from .database import init_db, get_session

app = FastAPI(title="Duff Digital Product Passport")

init_db()

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def root():
    return RedirectResponse(url="/frontend")


@app.post("/products", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, data: Product, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.get("/products", response_model=list[Product])
def list_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products
