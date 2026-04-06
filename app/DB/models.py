from decimal import Decimal
from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.DB.database import Base


class ProductDB(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    icon: Mapped[str] = mapped_column(String(10), default="📦")
