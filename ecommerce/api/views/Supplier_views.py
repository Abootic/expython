from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.Supplier_dto import SupplierDTO
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from api.dto.user_dto import UserDTO
from api.factories.service_factory import create_supplier_service  # Assuming service factory is used
from api.permissions.permissions import RoleRequiredPermission


class SupplierViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'SUPPLIER']  # Define roles allowed for this view

    def get_permissions(self):
        permission_classes = [IsAuthenticated, RoleRequiredPermission]
        return [permission() for permission in permission_classes]
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = create_supplier_service()  # Using service factory to inject the service

    def list(self, request):
        # Retrieve all suppliers using the service
        res = self._service.all()
        if res.status.succeeded:
            return Response([supplier.__dict__ for supplier in res.data], status=res.status.code)
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
            print("##############################################################")
            print(request.data.get('code'))
            # Create SupplierDTO from the request data
            supplier_dto = SupplierDTO(
                code=request.data.get('code'),
                market_id=request.data.get('market_id'),
                user_dto=user_dto
            )

            # Call the service to add the supplier and user
            result = self._service.add(supplier_dto)

            # Return success response with the created SupplierDTO data
            return Response(result.to_dict(), status=201)

        except Exception as e:
            # Handle any exception that occurs during the process
            return Response({"error": str(e)}, status=500)

    def update(self, request, pk=None):
        try:
            # Extract the customer data from the request body
            data = request.data
            user_dto_data = data.get('user_dto')

            # Ensure the user_dto is present and map it
            if user_dto_data:
                user_dto = UserDTO(**user_dto_data)  # Map user_dto data to UserDTO
            else:
                return Response({"error": "User data is required"}, status=400)

            # Create CustomerDTO
            print("22222222222222222222222222222222222222222222222222222222222")

            print(data.get('code'))
            customer_dto = SupplierDTO(
                id=data.get('id', pk),  # Use ID from request or from URL
                code=data.get('code'),
                user_id=data.get('user_id'),
                user_dto=user_dto  # Attach the UserDTO to the CustomerDTO
            )

            # Call the service to update the customer
            result = self._service.update(customer_dto)

            if result.status.succeeded:
                return Response(result.data.to_dict(), status=result.status.code)

            return Response({"error": result.status.message}, status=result.status.code)

        except Exception as e:
            return Response({"error": f"Error updating customer: {str(e)}"}, status=500)


    def destroy(self, request, pk=None):
        # Delete an existing supplier
        obj = SupplierDTO(id=pk)
        res = self._service.delete(obj)
        if res.status.succeeded:
            return Response({"message": "Supplier deleted"}, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)



    
    @action(detail=False, methods=['get'], url_path='supplierCountInmarket/(?P<marketid>\d+)')
    def supplierCountInmarket(self, request, marketid):
        # Call the service method to get the count of suppliers
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
            # Call the service method to get the supplier by code
            res = self._service.get_supplier_by_code(code)
            
            # Check if the service call was successful
            if res.status.succeeded:
                # Assuming `res.data` contains the supplier information
                return Response({"supplier_code": res.data.to_dict()}, status=res.status.code)
            
            # If the supplier wasn't found or some issue occurred
            return Response({"error": res.status.message}, status=res.status.code)
        
        except Exception as e:
            # If any error occurs, return a 500 error
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)
