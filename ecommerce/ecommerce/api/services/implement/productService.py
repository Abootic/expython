from api.repositories.interface.productRepositoryInterface import ProductRepositoryInterface
from api.services.interface.productServiceInterface import ProductServiceInterface
from api.dto.product_dto import ProductDTO
from api.models.product import Product
from typing import List

class ProductService(ProductServiceInterface):
  def __init__(self, product_repository: ProductRepositoryInterface):
      self.product_repository = product_repository

  def get_by_id(self, product_id: int) -> ProductDTO:
    product = self.product_repository.get_by_id(product_id)
    if product:
      return ProductDTO.from_model(product)
    return None

  def all(self) -> List[ProductDTO]:
        products = self.product_repository.all()
        return [ProductDTO.from_model(product) for product in products]

  def add(self, product_dto: ProductDTO) -> ProductDTO:
    product = Product(
      name=product_dto.name,
      price=product_dto.price,
      supplier_id=product_dto.supplier_id
    )
    added_product = self.product_repository.add(product)
    return ProductDTO.from_model(added_product)

  def update(self, product_dto: ProductDTO) -> ProductDTO:
    product = Product(
        id=product_dto.id,
        name=product_dto.name,
        price=product_dto.price,
        supplier_id=product_dto.supplier_id
    )
    updated_product = self.product_repository.update(product)
    return ProductDTO.from_model(updated_product)

  def delete(self, product_dto: ProductDTO) -> bool:
    product = Product.objects.get(id=product_dto.id)
    return self.product_repository.delete(product)
