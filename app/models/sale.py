"""
Modelo de dados para vendas
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Sale(Base):
    """
    Modelo para vendas
    """
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos (opcional - para uso futuro)
    # user = relationship("User", back_populates="sales")
    # product = relationship("Product", back_populates="sales")

    def __repr__(self):
        return f"<Sale(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, total={self.total_price})>"

    @property
    def discount_percentage(self) -> float:
        """Calcular percentual de desconto se houver"""
        if self.unit_price == 0:
            return 0.0
        # Aqui poderia comparar com preço original do produto
        # Por agora, retorna 0 (sem desconto)
        return 0.0

    def calculate_total(self) -> float:
        """Calcular total da venda"""
        return self.unit_price * self.quantity
