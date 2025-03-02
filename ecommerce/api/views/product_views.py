from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.product_dto import ProductDTO
from api.factories.service_factory import create_product_service

class ProductViewSet(viewsets.ViewSet):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.product_service = create_product_service()

  def list(self, request):
    products = self.product_service.all()
    product_dtos = [ProductDTO.from_model(product) for product in products]
    return Response([product.to_dict() for product in product_dtos])

  def retrieve(self, request, pk=None):
    product = self.product_service.get_by_id(pk)
    if product:
      product_dto = ProductDTO.from_model(product)
      return Response(product_dto.to_dict())
    return Response({"error": "Product not found"}, status=404)

  def create(self, request):
    product_dto = ProductDTO(name=request.data.get('name'), price=request.data.get('price'), supplier_id=request.data.get('supplier_id'))
    added_product = self.product_service.add(product_dto)
    return Response(added_product.to_dict(), status=201)

  def update(self, request, pk=None):
    product_dto = ProductDTO(id=pk, name=request.data.get('name'), price=request.data.get('price'), supplier_id=request.data.get('supplier_id'))
    updated_product = self.product_service.update(product_dto)
    return Response(updated_product.to_dict())

  def destroy(self, request, pk=None):
    product_dto = ProductDTO(id=pk)
    success = self.product_service.delete(product_dto)
    if success:
        return Response({"message": "Product deleted"}, status=204)
    return Response({"error": "Product not found"}, status=404)
