from decimal import Decimal
from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.order_dto import OrderDTO
from api.factories.service_factory import create_order_service
from api.models.order import Order
from rest_framework import status

class OrderViewSet(viewsets.ViewSet):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.order_service = create_order_service()

  def list(self, request):
    res = self.order_service.all()
    if res.status.succeeded:
          return Response([obj.to_dict() for obj in res.data], status=res.status.code)
    return Response({"error": res.status.message}, status=res.status.code)

  

  def retrieve(self, request, pk=None):
    order = self.order_service.get_by_id(pk)
    if order:
      order_dto = OrderDTO.from_model(order)
      return Response(order_dto.to_dict())
    return Response({"error": "Order not found"}, status=404)

  def create(self, request):
    try:
        # Create the OrderDTO from the request data
        order_dto = OrderDTO(
      id=request.data.get('id'),
      customer_id=request.data.get('customer_id'),  # ✅ Correct field name
      product_id=request.data.get('product_id'),
      total_price=Decimal(request.data.get('total_price')),
      price=Decimal(request.data.get('price')),
      create_at=request.data.get('create_at'),
      quantity=request.data.get('quantity')
  )


        # Call the add method of the service to add the order
        result = self.order_service.add(order_dto)

        if result.status.succeeded:
            # Return the success response with the order DTO
            return Response(result.data.to_dict(), status=201)

        return Response({"error": result.status.message}, status=result.status.code)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


  def update(self, request, pk=None):
    order_dto = OrderDTO(id=pk, customer_id=request.data.get('customer_id'), product_id=request.data.get('product_id'), total_price=request.data.get('total_price'), quantity=request.data.get('quantity'))
    order = Order(id=pk, customer_id=request.data.get('customer_id'), product_id=request.data.get('product_id'), total_price=request.data.get('total_price'), quantity=request.data.get('quantity'))
    updated_order = self.order_service.update(order)
    return Response(updated_order.to_dict())

  def destroy(self, request, pk=None):
    order = Order(id=pk)
    success = self.order_service.delete(order)
    if success:
        return Response({"message": "Order deleted"}, status=204)
    return Response({"error": "Order not found"}, status=404)
