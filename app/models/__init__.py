"""
Modelos de dados para o sistema de vendas
"""

# Importar Base para que esteja disponível
from ..database import Base

# Importar todos os modelos para que fiquem disponíveis
from .user import User
from .product import Product
from .sale import Sale

# Exportar para facilitar importação
__all__ = ["Base", "User", "Product", "Sale"]
