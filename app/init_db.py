"""
Script para inicializar o banco de dados
"""
from app.database import engine, Base
from app.models import User, Product, Sale
import logging

logger = logging.getLogger(__name__)


def create_tables():
    """
    Criar todas as tabelas no banco de dados
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso!")
        print("✅ Banco de dados inicializado com sucesso!")
        print("📋 Tabelas criadas:")
        print("   - users")
        print("   - products") 
        print("   - sales")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        print(f"❌ Erro ao inicializar banco: {e}")
        raise


def drop_tables():
    """
    Remover todas as tabelas (usar com cuidado!)
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Tabelas removidas com sucesso!")
        print("🗑️ Todas as tabelas foram removidas!")
    except Exception as e:
        logger.error(f"Erro ao remover tabelas: {e}")
        print(f"❌ Erro ao remover tabelas: {e}")
        raise


if __name__ == "__main__":
    print("🚀 Inicializando banco de dados SQLite...")
    create_tables()
