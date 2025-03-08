from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.factories.service_factory import get_service_factory
from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
from api.services.interfaces.ISupplierProfitService import ISupplierProfitService
from injector import inject


class SupplierProfitViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN']  # Define roles allowed for this view

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use ServiceFactory to get the service instance
        service_factory = get_service_factory()  # Singleton instance of ServiceFactory
        self._service = service_factory.create_supplier_profit_service(singleton=True)  # Get the service

    @permission_required_for_action({
        'create': [IsAuthenticated, RoleRequiredPermission],
        'list': [IsAuthenticated, RoleRequiredPermission],
    })
    def create(self, request):
        """
        Create or update the supplier profit for a given market and month.
        """
        market_id = request.data.get("market_id")
        month = request.data.get("month")

        # Basic validation for the input parameters
        if not market_id or not month:
            return Response({"error": "Market ID and month are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Call the service to update or create profit
            result = self._service.update_or_create_profit(market_id, month)

            # Check result and send appropriate response
            if result.status.succeeded:
                return Response({"message": "Supplier profit updated successfully"}, status=status.HTTP_200_OK)
            return Response({"error": result.status.message}, status=result.status.code)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
        List all supplier profits.
        """
        try:
            res = self._service.all()
            if res.status.succeeded:
                return Response([obj.to_dict() for obj in res.data], status=res.status.code)
            return Response({"error": res.status.message}, status=res.status.code)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
