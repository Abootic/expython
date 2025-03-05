from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.permissions.permissions import RoleRequiredPermission
from api.factories.service_factory import create_supplier_profit_repository

class SupplierProfitViewSet(viewsets.ViewSet):
    """
    A ViewSet for calculating and managing supplier profits.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the service using the factory
        self._service = create_supplier_profit_repository()

   # @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, RoleRequiredPermission])
    def create(self, request):
        market_id = request.data.get("market_id")
        month = request.data.get("month")
        profit = request.data.get("profit")  # ✅ Ensure profit is extracted

        if market_id is None or month is None or profit is None:
            return Response({"error": "market_id, month, and profit are required"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Pass all required arguments
        result = self._service.update_or_create_profit(market_id, month)

        return Response({"message": "Supplier profit updated successfully"}, status=status.HTTP_200_OK)
