"""
Rotas para gerenciamento de produtos
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas import Product, ProductCreate, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Criar um novo produto
    """
    try:
        return product_service.create_product(db, product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Product])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    Listar produtos com filtros
    """
    return product_service.get_products(db, skip=skip, limit=limit, active_only=active_only)


@router.get("/search", response_model=List[Product])
async def search_products(
    name: str = Query(..., description="Nome do produto para busca"),
    db: Session = Depends(get_db)
):
    """
    Buscar produtos por nome
    """
    return product_service.get_products_by_name(db, name)


@router.get("/in-stock", response_model=List[Product])
async def get_products_in_stock(db: Session = Depends(get_db)):
    """
    Obter produtos em estoque
    """
    return product_service.get_products_in_stock(db)


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obter produto por ID
    """
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int, 
    product_update: ProductUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualizar produto
    """
    try:
        product = product_service.update_product(db, product_id, product_update)
        if product is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{product_id}/stock")
async def update_stock(
    product_id: int,
    quantity_change: int = Query(..., description="Mudança no estoque (positivo para adicionar, negativo para remover)"),
    db: Session = Depends(get_db)
):
    """
    Atualizar estoque do produto
    """
    try:
        product = product_service.update_stock(db, product_id, quantity_change)
        if product is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {
            "message": "Estoque atualizado com sucesso",
            "product_id": product_id,
            "new_stock": product.stock_quantity,
            "change": quantity_change
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Deletar produto (soft delete)
    """
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}


@router.delete("/{product_id}/hard")
async def hard_delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Deletar produto permanentemente
    """
    success = product_service.hard_delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto removido permanentemente"}
