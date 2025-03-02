from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.customer_dto import CustomerDTO
from rest_framework.permissions import IsAuthenticated

from api.factories.service_factory import create_customer_service  # Assuming service factory is used
from api.permissions import permission_required_for_action
from api.permissions.permissions import RoleRequiredPermission


class CustomerViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'Customer']  # Define roles allowed for this view
     # Define roles allowed for this view

    @permission_required_for_action({
        'create': [],
        'list': [IsAuthenticated, RoleRequiredPermission],
        'retrieve': [IsAuthenticated, RoleRequiredPermission],
        'update': [IsAuthenticated, RoleRequiredPermission],
        'destroy': [IsAuthenticated, RoleRequiredPermission]
    })
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = create_customer_service()  # Using service factory to inject the service

    def list(self, request):
        # Retrieve all suppliers using the service
        res = self._service.all()
        if res.status.succeeded:
            return Response([supplier.to_dict() for supplier in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def retrieve(self, request, pk=None):
        # Retrieve a single supplier by ID
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def create(self, request):
        try:
            # Extract user and supplier data from the request
            user_dto = request.data.get('user_dto')  # Nested user data in the request
            if not user_dto:
                return Response({"error": "User data is required"}, status=400)

            # Create SupplierDTO from the request data
            CUSTOMER_DTO = CustomerDTO(
                code=request.data.get('code'),
                user_dto=user_dto
            )

            # Call the service to add the supplier and user
            result = self._service.add(CUSTOMER_DTO)

            # Return success response with the created SupplierDTO data
            return Response(result.to_dict(), status=201)

        except Exception as e:
            # Handle any exception that occurs during the process
            return Response({"error": str(e)}, status=500)


    def update(self, request, pk=None):
        # Update an existing supplier
        obj = CustomerDTO(id=pk, code=request.data.get('code'))
        res = self._service.update(obj)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def destroy(self, request, pk=None):
        # Delete an existing supplier
        obj = CustomerDTO(id=pk)
        res = self._service.delete(obj)
        if res.status.succeeded:
            return Response({"message": "Supplier deleted"}, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)
