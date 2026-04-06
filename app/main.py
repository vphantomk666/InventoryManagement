from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
import jinja2
import os

from app.DB.database import SessionLocal, engine, Base
from app.DB.models import ProductDB as Product
from app.schemas.schemas import ProductCreate, ProductResponse

Base.metadata.create_all(bind=engine)

# Seed initial data
def seed_initial_data():
    db = SessionLocal()
    try:
        existing_products = db.query(Product).count()
        if existing_products == 0:
            from decimal import Decimal
            products = [
                Product(
                    name="Laptop",
                    description="High-performance laptop for work and gaming",
                    price=Decimal("999.99"),
                    quantity=10,
                    icon="💻"
                ),
                Product(
                    name="Mouse",
                    description="Wireless ergonomic mouse",
                    price=Decimal("29.99"),
                    quantity=50,
                    icon="🖱️"
                ),
                Product(
                    name="Keyboard",
                    description="Mechanical keyboard with RGB lighting",
                    price=Decimal("79.99"),
                    quantity=25,
                    icon="⌨️"
                ),
                Product(
                    name="Monitor",
                    description="27-inch 4K monitor",
                    price=Decimal("349.99"),
                    quantity=15,
                    icon="🖥️"
                ),
                Product(
                    name="Headphones",
                    description="Noise-cancelling wireless headphones",
                    price=Decimal("149.99"),
                    quantity=30,
                    icon="🎧"
                )
            ]
            for product in products:
                db.add(product)
            db.commit()
            print("Initial data seeded.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

seed_initial_data()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

STATIC_DIR = FRONTEND_DIR / "static"
TEMPLATES_DIR = FRONTEND_DIR / "templates"

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)), auto_reload=False
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    products_data = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "quantity": p.quantity,
            "icon": p.icon or "📦",
        }
        for p in products
    ]
    template = jinja_env.get_template("index.html")
    return HTMLResponse(template.render(request=request, products=products_data))


@app.get("/db-test")
def db_test():
    return {"db": "connected"}


#  API ROUTES
@app.get("/products/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Deleted"}
