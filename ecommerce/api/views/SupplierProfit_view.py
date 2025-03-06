from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.permissions.permissions import RoleRequiredPermission
from api.factories.service_factory import create_supplier_profit_service
from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
from rest_framework.permissions import IsAuthenticated

class SupplierProfitViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN']  # Define roles allowed for this view


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the service using the factory
        self._service = create_supplier_profit_service()
    @permission_required_for_action({
          'create': [IsAuthenticated, RoleRequiredPermission],
          'list': [IsAuthenticated, RoleRequiredPermission],
       
      })

   # @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, RoleRequiredPermission])
    def create(self, request):
        market_id = request.data.get("market_id")
        month = request.data.get("month")
        result = self._service.update_or_create_profit(market_id, month)

        return Response({"message": "Supplier profit updated successfully"}, status=status.HTTP_200_OK)
    def list(self, request):
        # Retrieve all suppliers using the service
        res = self._service.all()
        if res.status.succeeded:
            return Response([obj.to_dict() for obj in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)
