from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.customer_dto import CustomerDTO
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from api.dto.user_dto import UserDTO
from api.services.interfaces.IcustomerService import ICustomerService
from api.factories.service_factory import get_service_factory  # Import ServiceFactory
from api.permissions.permission_required_for_action import permission_required_for_action
from api.permissions.permissions import RoleRequiredPermission
from api.validation.validation_request import ValidationRequest



class CustomerViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'Customer']
    def get_permissions(self):
         
            if self.action == 'create':
                return []  # No permissions required for 'create' action

        
            return [permission() for permission in self.permission_classes]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get the service from the ServiceFactory
        service_factory = get_service_factory()
        self._service = service_factory.create_customer_service(singleton=True)  # Get the singleton instance

    @permission_required_for_action({
        'get_customer_by_code': [IsAuthenticated, RoleRequiredPermission],
    })

    @action(detail=False, methods=['get'], url_path=r'get_customer_by_code/(?P<code>[\w-]+)')
    def get_customer_by_code(self, request, code):
        try:
            # Call the service method to get the customer by code
            res = self._service.get_customer_by_code(code)
            
            if res.status.succeeded:
                return Response({"customer_code": res.data.to_dict()}, status=res.status.code)
            
            return Response({"error": res.status.message}, status=res.status.code)
        
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)


    @permission_required_for_action({
        'list': [IsAuthenticated, RoleRequiredPermission],
    })
    def list(self, request):
        res = self._service.all()
        if res.status.succeeded:
            return Response([customer.to_dict() for customer in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    @permission_required_for_action({
        'retrieve': [IsAuthenticated, RoleRequiredPermission],
    })
    def retrieve(self, request, pk=None):
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)
    
   
  

    def create(self, request):
        print(f"Received Data: {request.data}")
        try:
            # Define required fields
            required_fields = ['code', 'user']
            user_dto_required_fields = ['username', 'email', 'user_type', 'password']

            # Validate main request data
            validation_error = ValidationRequest.validate_request_data(request.data, required_fields)
            if validation_error:
                return validation_error

            # Validate 'user' data
            user_dto_data = request.data.get('user')
            validation_error = ValidationRequest.validate_request_data(user_dto_data, user_dto_required_fields)
            if validation_error:
                return validation_error

            # Create UserDTO
            user_dto = UserDTO(**{field: user_dto_data[field] for field in user_dto_required_fields})

            # Create CustomerDTO
            customer_dto = CustomerDTO(code=request.data['code'], user_dto=user_dto)

            # Call the service to add the customer
            result = self._service.add(customer_dto)

            # Return response based on operation result
            response_data = {
                'succeeded': result.status.succeeded,
                'message': result.status.message,
                'data': {'message': result.data}  # Ensure 'data' is always an object
            }
            print("Customer created successfully!" if result.status.succeeded else f"Customer creation failed: {result.status.message}")
            return Response(response_data, status=200)

        except Exception as e:
            # Handle unexpected errors
            print(f"Exception occurred: {str(e)}")
            return Response({"error": str(e)}, status=500)
    
    @permission_required_for_action({
        'update': [IsAuthenticated, RoleRequiredPermission],
    })
    def update(self, request, pk=None):
        try:
            data = request.data
            user_dto_data = data.get('user_dto')

            if user_dto_data:
                user_dto = UserDTO(**user_dto_data)
            else:
                return Response({"error": "User data is required"}, status=400)

            customer_dto = CustomerDTO(id=data.get('id', pk), code=data.get('code'), user_dto=user_dto)
            result = self._service.update(customer_dto)

            if result.status.succeeded:
                return Response(result.data.to_dict(), status=result.status.code)
            return Response({"error": result.status.message}, status=result.status.code)

        except Exception as e:
            return Response({"error": f"Error updating customer: {str(e)}"}, status=500)
        
    @permission_required_for_action({
        'destroy': [IsAuthenticated, RoleRequiredPermission],
    })

    def destroy(self, request, pk=None):
        customer_dto = CustomerDTO(id=pk)
        res = self._service.delete(customer_dto)
        if res.status.succeeded:
            return Response({"message": "Customer deleted"}, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)
