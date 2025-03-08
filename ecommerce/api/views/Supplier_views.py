from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.Supplier_dto import SupplierDTO
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from api.dto.user_dto import UserDTO
from api.services.interfaces.ISupplierService import ISupplierService
from api.permissions.permissions import RoleRequiredPermission
from api.factories.service_factory import get_service_factory  # Import the factory


class SupplierViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'SUPPLIER']  # Define roles allowed for this view

    def get_permissions(self):
        """
        Handle permissions per action.
        """
        permission_classes = [IsAuthenticated, RoleRequiredPermission]
        return [permission() for permission in permission_classes]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use ServiceFactory to get the service instance
        service_factory = get_service_factory()  # Singleton instance of ServiceFactory
        self._service = service_factory.create_supplier_service(singleton=True)  # Get the service

    def list(self, request):
        """
        Retrieve all suppliers.
        """
        res = self._service.all()
        if res.status.succeeded:
            return Response([supplier.__dict__ for supplier in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single supplier by ID.
        """
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def create(self, request):
        """
        Create a new supplier.
        """
        try:
            # Extract user and supplier data from the request
            user_dto_data = request.data.get('user_dto')
            if not user_dto_data:
                return Response({"error": "User data is required"}, status=400)

            user_dto = UserDTO(**user_dto_data)  # Map user data to UserDTO

            # Create SupplierDTO from the request data
            supplier_dto = SupplierDTO(
                code=request.data.get('code'),
                market_id=request.data.get('market_id'),
                user_dto=user_dto
            )

            # Call the service to add the supplier and user
            result = self._service.add(supplier_dto)

            if result.status.succeeded:
                return Response(result.data.to_dict(), status=201)

            return Response({"error": result.status.message}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def update(self, request, pk=None):
        """
        Update an existing supplier.
        """
        try:
            data = request.data
            user_dto_data = data.get('user_dto')

            # Validate user_dto presence
            if user_dto_data:
                user_dto = UserDTO(**user_dto_data)
            else:
                return Response({"error": "User data is required"}, status=400)

            # Create SupplierDTO with the provided data
            supplier_dto = SupplierDTO(
                id=data.get('id', pk),
                code=data.get('code'),
                user_dto=user_dto
            )

            # Call the service to update the supplier
            result = self._service.update(supplier_dto)

            if result.status.succeeded:
                return Response(result.data.to_dict(), status=result.status.code)

            return Response({"error": result.status.message}, status=result.status.code)

        except Exception as e:
            return Response({"error": f"Error updating supplier: {str(e)}"}, status=500)

    def destroy(self, request, pk=None):
        """
        Delete an existing supplier.
        """
        try:
            supplier_dto = SupplierDTO(id=pk)
            res = self._service.delete(supplier_dto)

            if res.status.succeeded:
                return Response({"message": "Supplier deleted successfully"}, status=204)
            return Response({"error": res.status.message}, status=res.status.code)

        except Exception as e:
            return Response({"error": f"Error deleting supplier: {str(e)}"}, status=500)

    @action(detail=False, methods=['get'], url_path='supplierCountInmarket/(?P<marketid>\d+)')
    def supplierCountInmarket(self, request, marketid):
        """
        Custom action to get the supplier count by market ID.
        """
        res = self._service.count_by_market_id(marketid)
        if res.status.succeeded:
            return Response({"supplier_count": res.data}, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    @action(detail=False, methods=['get'], url_path=r'get_supplier_by_code/(?P<code>[\w-]+)')
    def get_supplier_by_code(self, request, code):
        """
        Custom action to retrieve supplier by code.
        """
        try:
            res = self._service.get_supplier_by_code(code)

            if res.status.succeeded:
                return Response({"supplier_code": res.data.to_dict()}, status=res.status.code)

            return Response({"error": res.status.message}, status=res.status.code)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)
