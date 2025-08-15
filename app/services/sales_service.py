"""
Serviços para gerenciamento de vendas
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from app.models import Sale as SaleModel, Product as ProductModel, User as UserModel
from app.schemas import Sale, SaleCreate
from app.services.product_service import update_stock


def create_sale(db: Session, sale: SaleCreate) -> SaleModel:
    """
    Criar uma nova venda
    """
    # Verificar se usuário existe
    user = db.query(UserModel).filter(UserModel.id == sale.user_id).first()
    if not user:
        raise ValueError("Usuário não encontrado")
    
    # Verificar se produto existe e está ativo
    product = db.query(ProductModel).filter(
        ProductModel.id == sale.product_id,
        ProductModel.is_active == True
    ).first()
    if not product:
        raise ValueError("Produto não encontrado ou inativo")
    
    # Verificar estoque
    if product.stock_quantity < sale.quantity:
        raise ValueError(f"Estoque insuficiente. Disponível: {product.stock_quantity}")
    
    # Calcular preços
    unit_price = sale.unit_price if sale.unit_price else product.price
    total_price = unit_price * sale.quantity
    
    # Criar venda
    db_sale = SaleModel(
        user_id=sale.user_id,
        product_id=sale.product_id,
        quantity=sale.quantity,
        unit_price=unit_price,
        total_price=total_price
    )
    
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    # Atualizar estoque
    try:
        update_stock(db, sale.product_id, -sale.quantity)
    except ValueError as e:
        # Rollback da venda se não conseguir atualizar estoque
        db.delete(db_sale)
        db.commit()
        raise e
    
    return db_sale


def get_sale(db: Session, sale_id: int) -> Optional[SaleModel]:
    """
    Obter venda por ID
    """
    return db.query(SaleModel).filter(SaleModel.id == sale_id).first()


def get_sales(db: Session, skip: int = 0, limit: int = 100) -> List[SaleModel]:
    """
    Listar todas as vendas
    """
    return db.query(SaleModel).offset(skip).limit(limit).all()


def get_sales_by_user(db: Session, user_id: int) -> List[SaleModel]:
    """
    Obter vendas de um usuário específico
    """
    return db.query(SaleModel).filter(SaleModel.user_id == user_id).all()


def get_sales_by_product(db: Session, product_id: int) -> List[SaleModel]:
    """
    Obter vendas de um produto específico
    """
    return db.query(SaleModel).filter(SaleModel.product_id == product_id).all()


def get_sales_by_date_range(db: Session, start_date: date, end_date: date) -> List[SaleModel]:
    """
    Obter vendas em um período específico
    """
    return db.query(SaleModel).filter(
        SaleModel.sale_date >= start_date,
        SaleModel.sale_date <= end_date
    ).all()


def get_sales_today(db: Session) -> List[SaleModel]:
    """
    Obter vendas do dia atual
    """
    today = date.today()
    return get_sales_by_date_range(db, today, today)


def get_total_sales_value(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> float:
    """
    Calcular valor total de vendas em um período
    """
    query = db.query(SaleModel)
    
    if start_date:
        query = query.filter(SaleModel.sale_date >= start_date)
    if end_date:
        query = query.filter(SaleModel.sale_date <= end_date)
    
    sales = query.all()
    return sum(sale.total_price for sale in sales)


def get_sales_summary(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> dict:
    """
    Obter resumo de vendas
    """
    query = db.query(SaleModel)
    
    if start_date:
        query = query.filter(SaleModel.sale_date >= start_date)
    if end_date:
        query = query.filter(SaleModel.sale_date <= end_date)
    
    sales = query.all()
    
    if not sales:
        return {
            "total_sales": 0,
            "total_value": 0.0,
            "total_quantity": 0,
            "average_sale_value": 0.0
        }
    
    total_sales = len(sales)
    total_value = sum(sale.total_price for sale in sales)
    total_quantity = sum(sale.quantity for sale in sales)
    average_sale_value = total_value / total_sales if total_sales > 0 else 0.0
    
    return {
        "total_sales": total_sales,
        "total_value": total_value,
        "total_quantity": total_quantity,
        "average_sale_value": average_sale_value
    }


def cancel_sale(db: Session, sale_id: int) -> bool:
    """
    Cancelar venda (estornar estoque)
    """
    sale = db.query(SaleModel).filter(SaleModel.id == sale_id).first()
    
    if not sale:
        return False
    
    # Estornar estoque
    try:
        update_stock(db, sale.product_id, sale.quantity)
    except ValueError:
        # Se não conseguir estornar, apenas remove a venda
        pass
    
    # Remover venda
    db.delete(sale)
    db.commit()
    return True
