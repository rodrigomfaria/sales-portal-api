"""
Rotas para gerenciamento de vendas
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.schemas import Sale, SaleCreate
from app.services import sales_service

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/", response_model=Sale)
async def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """
    Criar uma nova venda
    """
    try:
        return sales_service.create_sale(db, sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Sale])
async def list_sales(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Listar todas as vendas
    """
    return sales_service.get_sales(db, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[Sale])
async def get_sales_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obter vendas de um usuário específico
    """
    return sales_service.get_sales_by_user(db, user_id)


@router.get("/product/{product_id}", response_model=List[Sale])
async def get_sales_by_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obter vendas de um produto específico
    """
    return sales_service.get_sales_by_product(db, product_id)


@router.get("/date-range")
async def get_sales_by_date_range(
    start_date: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obter vendas em um período específico
    """
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Data inicial deve ser anterior à data final")
    
    sales = sales_service.get_sales_by_date_range(db, start_date, end_date)
    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_sales": len(sales),
        "sales": sales
    }


@router.get("/today", response_model=List[Sale])
async def get_sales_today(db: Session = Depends(get_db)):
    """
    Obter vendas do dia atual
    """
    return sales_service.get_sales_today(db)


@router.get("/summary")
async def get_sales_summary(
    start_date: Optional[date] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obter resumo de vendas
    """
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="Data inicial deve ser anterior à data final")
    
    summary = sales_service.get_sales_summary(db, start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "summary": summary
    }


@router.get("/total-value")
async def get_total_sales_value(
    start_date: Optional[date] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Calcular valor total de vendas
    """
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="Data inicial deve ser anterior à data final")
    
    total_value = sales_service.get_total_sales_value(db, start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "total_value": total_value
    }


@router.get("/{sale_id}", response_model=Sale)
async def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """
    Obter venda por ID
    """
    sale = sales_service.get_sale(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale


@router.delete("/{sale_id}")
async def cancel_sale(sale_id: int, db: Session = Depends(get_db)):
    """
    Cancelar venda (estornar estoque)
    """
    success = sales_service.cancel_sale(db, sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"message": "Venda cancelada com sucesso"}
