from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.product_dto import ProductDTO
from api.factories.service_factory import create_product_service

class ProductViewSet(viewsets.ViewSet):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.product_service = create_product_service()

  def list(self, request):
      res = self.product_service.all()
      if res.status.succeeded:
            return Response([obj.to_dict() for obj in res.data], status=res.status.code)
      return Response({"error": res.status.message}, status=res.status.code)

  def retrieve(self, request, pk=None):
      res = self.product_service.get_by_id(pk)
        
      if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)

      return Response({"error": res.status.message}, status=res.status.code)
  def create(self, request):
    try:
        # Creating the ProductDTO from the request data
        product_dto = ProductDTO(
            name=request.data.get('name'),
            price=request.data.get('price'),
            supplier_id=request.data.get('supplier_id')
        )

        # Call the add method of the service to add the product
        res = self.product_service.add(product_dto)

        # Ensure the response is a dictionary, so it's serializable
        return Response(res.data.to_dict(), status=201)  # Assuming res.data is a ProductDTO
    except Exception as e:
        # Handle any exception that occurs during the process
        return Response({"error": str(e)}, status=500)




  def update(self, request, pk=None):
       pro = ProductDTO(id=pk, name=request.data.get('name'), price=request.data.get('price'), supplier_id=request.data.get('supplier_id'))
       res=self.product_service.update(pro)
       if res.status.succeeded:
           

            return Response(res.data.to_dict(), status=res.status.code)
       return Response({"error": res.status.message}, status=res.status.code)

  def destroy(self, request, pk=None):
    product_dto = ProductDTO(id=pk)
    success = self.product_service.delete(product_dto)
    if success:
        return Response({"message": "Product deleted"}, status=204)
    return Response({"error": "Product not found"}, status=404)
