"""
Modelo de dados para produtos
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """
    Modelo para produtos
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock_quantity})>"

    @property
    def is_in_stock(self):
        """Verificar se produto está em estoque"""
        return self.stock_quantity > 0 and self.is_active

    def can_sell(self, quantity: int) -> bool:
        """Verificar se é possível vender a quantidade solicitada"""
        return self.is_active and self.stock_quantity >= quantity
