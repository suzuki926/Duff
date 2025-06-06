from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from .models import Product, Request, RequestURL, RequestCreate, RequestRead, RequestURLRead
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


@app.post("/requests", response_model=RequestRead)
def create_request(data: RequestCreate, session: Session = Depends(get_session)):
    req = Request(content=data.content)
    session.add(req)
    session.commit()
    session.refresh(req)
    url = RequestURL(request_id=req.id, tier=1)
    session.add(url)
    session.commit()
    session.refresh(req)
    return req


@app.post("/requests/{request_id}/escalate", response_model=RequestURLRead)
def escalate_request(request_id: int, session: Session = Depends(get_session)):
    req = session.get(Request, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.tier >= 3:
        raise HTTPException(status_code=400, detail="Already at highest tier")
    req.tier += 1
    url = RequestURL(request_id=req.id, tier=req.tier)
    session.add(url)
    session.add(req)
    session.commit()
    session.refresh(url)
    return url


@app.get("/requests", response_model=list[RequestRead])
def list_requests(session: Session = Depends(get_session)):
    requests = session.exec(select(Request)).all()
    for r in requests:
        r.urls  # triggers loading of relationship
    return requests
