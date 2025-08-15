"""
Rotas para gerenciamento de usuários
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User as UserModel
from app.schemas import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Criar um novo usuário
    """
    # Verificar se email já existe
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar novo usuário
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[User])
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Listar todos os usuários
    """
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obter usuário por ID
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Atualizar usuário
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualizar apenas campos fornecidos
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletar usuário
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(user)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}
