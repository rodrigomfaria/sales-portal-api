"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Schemas para User
class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schemas para Product
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None


class Product(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schemas para Sale
class SaleBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    unit_price: Optional[float] = None  # Se não fornecido, usa preço do produto
    total_price: Optional[float] = None  # Calculado automaticamente


class SaleCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    unit_price: Optional[float] = None  # Opcional - usa preço do produto se não fornecido


class Sale(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    sale_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
