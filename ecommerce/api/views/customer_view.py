from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.customer_dto import CustomerDTO
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from api.dto.user_dto import UserDTO
from api.services.interfaces.IcustomerService import ICustomerService
from api.factories.service_factory import get_service_factory  # Import ServiceFactory

class CustomerViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'Customer']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get the service from the ServiceFactory
        service_factory = get_service_factory()
        self._service = service_factory.create_customer_service(singleton=True)  # Get the singleton instance

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

    def list(self, request):
        res = self._service.all()
        if res.status.succeeded:
            return Response([customer.to_dict() for customer in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def retrieve(self, request, pk=None):
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def create(self, request):
        try:
            user_dto = request.data.get('user_dto')
            if not user_dto:
                return Response({"error": "User data is required"}, status=400)

            customer_dto = CustomerDTO(code=request.data.get('code'), user_dto=user_dto)
            result = self._service.add(customer_dto)
            return Response(result.to_dict(), status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

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

    def destroy(self, request, pk=None):
        customer_dto = CustomerDTO(id=pk)
        res = self._service.delete(customer_dto)
        if res.status.succeeded:
            return Response({"message": "Customer deleted"}, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)
