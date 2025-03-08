from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.percentage_dto import PercentageDTO
from api.services.interfaces.IPercentageService import IPercentageService
from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from injector import inject
from api.factories.service_factory import ServiceFactory, get_service_factory  # Import your service factory

class PercentageViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN']  # Define roles allowed for this view

  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize service using service_factory if not injected directly
        service_factory = ServiceFactory()
        self._service = service_factory.create_percentage_service(singleton=True)


    @permission_required_for_action({
        'create': [IsAuthenticated, RoleRequiredPermission],
        'list': [IsAuthenticated, RoleRequiredPermission],
        'retrieve': [IsAuthenticated, RoleRequiredPermission],
        'update': [IsAuthenticated, RoleRequiredPermission],
        'destroy': [IsAuthenticated, RoleRequiredPermission]
    })
    def list(self, request):
        """
        Retrieve a list of all percentages.
        """
        res = self._service.all()
        if res.status.succeeded:
            return Response([obj.__dict__ for obj in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific percentage by ID.
        """
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def create(self, request):
        """
        Create a new percentage entry.
        """
        try:
            percentage_dto = PercentageDTO(
                supplier_id=request.data.get('supplier_id'),
                market_id=request.data.get('market_id'),
                priority=request.data.get('priority'),
                percentage_value=request.data.get('percentage_value')
            )
            res = self._service.add(percentage_dto)
            if res.status.succeeded:
                return Response(res.status.message, status=201)
            return Response({"error": res.status.message}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def update(self, request, pk=None):
        """
        Update an existing percentage entry.
        """
        try:
            percentage_dto = PercentageDTO(
                id=pk,
                supplier_id=request.data.get('supplier_id'),
                market_id=request.data.get('market_id'),
                priority=request.data.get('priority'),
                percentage_value=request.data.get('percentage_value')
            )
            res = self._service.update(percentage_dto)
            if res.status.succeeded:
                return Response(res.status.message, status=res.status.code)
            return Response({"error": res.status.message}, status=res.status.code)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def destroy(self, request, pk=None):
        """
        Delete an existing percentage entry.
        """
        try:
            percentage_dto = PercentageDTO(id=pk)
            success = self._service.delete(percentage_dto)
            if success:
                return Response(success.status.message, status=204)
            return Response({"error": success.status.message}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @action(detail=False, methods=['POST'], url_path='assign_percentage_value_to_suppliers/(?P<market_id>\d+)')
    def assign_percentage_value_to_suppliers(self, request, market_id=None):
        """
        Assign percentage value to suppliers based on the market.
        """
        try:
            success = self._service.assign_percentage_value_to_suppliers(market_id)
            if success:
                return Response(success.status.message, status=204)
            return Response({"error": success.status.message}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
