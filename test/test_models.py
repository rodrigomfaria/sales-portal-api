"""
Testes unitários para modelos de dados
"""
import unittest
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import User, Product, Sale
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker


class TestModels(unittest.TestCase):
    """
    Testes para os modelos de dados
    """
    
    @classmethod
    def setUpClass(cls):
        """Configurar banco de testes"""
        # Usar banco em memória para testes
        cls.test_engine = engine
        cls.TestSessionLocal = SessionLocal
        
    def setUp(self):
        """Configurar cada teste"""
        self.db = self.TestSessionLocal()
        
    def tearDown(self):
        """Limpar após cada teste"""
        self.db.close()
        
    def test_create_user(self):
        """Testar criação de usuário"""
        user = User(
            name="Test User",
            email="test@example.com",
            is_active=True
        )
        
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        
    def test_create_product(self):
        """Testar criação de produto"""
        product = Product(
            name="Test Product",
            description="A test product",
            price=99.99,
            stock_quantity=10,
            is_active=True
        )
        
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.stock_quantity, 10)
        
    def test_create_sale(self):
        """Testar criação de venda"""
        sale = Sale(
            user_id=1,
            product_id=1,
            quantity=2,
            unit_price=50.0,
            total_price=100.0
        )
        
        self.assertEqual(sale.user_id, 1)
        self.assertEqual(sale.product_id, 1)
        self.assertEqual(sale.quantity, 2)
        self.assertEqual(sale.total_price, 100.0)


if __name__ == "__main__":
    unittest.main()
