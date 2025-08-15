"""
Serviços para gerenciamento de produtos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Product as ProductModel
from app.schemas import Product, ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate) -> ProductModel:
    """
    Criar um novo produto
    """
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Optional[ProductModel]:
    """
    Obter produto por ID
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[ProductModel]:
    """
    Listar produtos com filtros
    """
    query = db.query(ProductModel)
    
    if active_only:
        query = query.filter(ProductModel.is_active == True)
    
    return query.offset(skip).limit(limit).all()


def get_products_by_name(db: Session, name: str) -> List[ProductModel]:
    """
    Buscar produtos por nome (busca parcial)
    """
    return db.query(ProductModel).filter(
        ProductModel.name.contains(name),
        ProductModel.is_active == True
    ).all()


def get_products_in_stock(db: Session) -> List[ProductModel]:
    """
    Obter produtos em estoque
    """
    return db.query(ProductModel).filter(
        ProductModel.stock_quantity > 0,
        ProductModel.is_active == True
    ).all()


def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[ProductModel]:
    """
    Atualizar produto
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        return None
    
    # Atualizar apenas campos fornecidos
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


def update_stock(db: Session, product_id: int, quantity_change: int) -> Optional[ProductModel]:
    """
    Atualizar estoque do produto (pode ser positivo ou negativo)
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        return None
    
    new_quantity = db_product.stock_quantity + quantity_change
    
    # Não permitir estoque negativo
    if new_quantity < 0:
        raise ValueError("Estoque não pode ficar negativo")
    
    db_product.stock_quantity = new_quantity
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """
    Deletar produto (soft delete - marcar como inativo)
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        return False
    
    db_product.is_active = False
    db.commit()
    return True


def hard_delete_product(db: Session, product_id: int) -> bool:
    """
    Deletar produto permanentemente
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True
