from typing import Optional
from api.models.product import Product

class ProductDTO:
  def __init__(self, id: Optional[int] = None, supplier_id: Optional[int] = None, name: Optional[str] = None, price: Optional[float] = None):
    self.id = id
    self.supplier_id = supplier_id
    self.name = name
    self.price = price

  @classmethod
  def from_model(cls, product: Product) -> 'ProductDTO':
    return cls(
      id=product.id,
      supplier_id=product.supplier.id if product.supplier else None,
      name=product.name,
      price=product.price
    )

  def to_dict(self) -> dict:
    return {
      'id': self.id,
      'supplier_id': self.supplier_id,
      'name': self.name,
      'price': str(self.price)
    }

  def __str__(self) -> str:
    return f"ProductDTO(id={self.id}, supplier_id={self.supplier_id}, name='{self.name}', price={self.price})"
