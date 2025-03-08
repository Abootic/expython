from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.dto.order_dto import OrderDTO
from api.services.interfaces.IorderService import IOrderService
from api.Mapper.OrderMapper import OrderMapper  # Assuming this is used for DTO transformation
from rest_framework.decorators import action
from api.factories.service_factory import ServiceFactory  # Import ServiceFactory

class OrderViewSet(viewsets.ViewSet):

    def __init__(self, *args, **kwargs):
        """
        Initialize the OrderViewSet with the OrderService created by ServiceFactory.
        """
        service_factory = ServiceFactory()  # Create an instance of ServiceFactory
        self.order_service = service_factory.create_order_service(singleton=True)  # Use the factory to get the service
        super().__init__(*args, **kwargs)

    def list(self, request):
        """
        Retrieve a list of all orders.
        """
        res = self.order_service.all()
        if res.status.succeeded:
            return Response([obj.__dict__ for obj in res.data], status=status.HTTP_200_OK)
        return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific order by ID.
        """
        res = self.order_service.get_by_id(pk)
        if res.status.succeeded:
            order_dto = OrderDTO.from_model(res.data)  # Map to DTO
            return Response(order_dto.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        Create a new order.
        """
        order_data = request.data
        try:
            order_dto = OrderDTO(**order_data)
            res = self.order_service.add(order_dto)
            if res.status.succeeded:
                return Response(res.status.message, status=status.HTTP_201_CREATED)
            return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update an existing order.
        """
        order_data = request.data
        try:
            order_dto = OrderDTO(**order_data)
            order_dto.id = pk
            res = self.order_service.update(order_dto)
            if res.status.succeeded:
                order_dto = OrderDTO.from_model(res.data)
                return Response(order_dto.to_dict(), status=status.HTTP_200_OK)
            return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete an existing order.
        """
        try:
            res = self.order_service.get_by_id(pk)
            if res.status.succeeded:
                order = res.data
                delete_result = self.order_service.delete(order)
                if delete_result.status.succeeded:
                    return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                return Response({"error": delete_result.status.message}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='calculate-profit', url_name='calculate-profit')
    def calculate_profit(self, request, pk=None):
        """
        Calculate and update the supplier profit based on an order.
        """
        res = self.order_service.calculate_supplier_profit(pk)
        if res.status.succeeded:
            return Response({"message": "Profit calculated and updated successfully", "data": res.data}, status=status.HTTP_200_OK)
        return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)

    def process_order(self, request, pk=None):
        """
        Process an order, including calculating profit and updating the supplier.
        """
        res = self.order_service.process_order(pk)
        if res.status.succeeded:
            return Response({"message": "Order processed successfully"}, status=status.HTTP_200_OK)
        return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)

    def get_supplier_profit(self, request, supplier_id=None, month=None):
        """
        Retrieve the supplier's profit for a specific month.
        """
        res = self.order_service.get_supplier_profit_for_month(supplier_id, month)
        if res.status.succeeded:
            return Response({"profit": res.data}, status=status.HTTP_200_OK)
        return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)
