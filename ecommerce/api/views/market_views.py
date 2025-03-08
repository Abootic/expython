from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.market_dto import MarketDTO
from rest_framework.permissions import IsAuthenticated
from api.factories.service_factory import get_service_factory  # Import ServiceFactory

class MarketViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'Market']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get the service from the ServiceFactory
        service_factory = get_service_factory()
        self._service = service_factory.create_market_service(singleton=True)  # Get the singleton instance

    def list(self, request):
        res = self._service.all()
        if res.status.succeeded:
            return Response([market.to_dict() for market in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def retrieve(self, request, pk=None):
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def create(self, request):
        try:
            market_dto = MarketDTO(name=request.data.get('name'))
            result = self._service.add(market_dto)
            return Response(result.to_dict(), status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def update(self, request, pk=None):
        try:
            market_dto = MarketDTO(id=pk, name=request.data.get('name'))
            result = self._service.update(market_dto)
            return Response(result.to_dict(), status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def destroy(self, request, pk=None):
        market_dto = MarketDTO(id=pk)
        res = self._service.delete(market_dto)
        if res:
            return Response({"message": "Market deleted"}, status=200)
        return Response({"error": "Market not found"}, status=404)
