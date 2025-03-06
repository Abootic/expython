from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.market_dto import MarketDTO
from api.factories.service_factory import create_market_service
from rest_framework.permissions import IsAuthenticated

from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
class MarketViewSet(viewsets.ViewSet):
  required_roles = ['ADMIN', 'SUPPLIER']  # Define roles allowed for this view

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.market_service = create_market_service()

  @permission_required_for_action({
          'create': [],
          'list': [IsAuthenticated, RoleRequiredPermission],
          'retrieve': [IsAuthenticated, RoleRequiredPermission],
          'update': [IsAuthenticated, RoleRequiredPermission],
          'destroy': [IsAuthenticated, RoleRequiredPermission],
          'get_customer_by_code': [IsAuthenticated, RoleRequiredPermission]
      })

  def list(self, request):
    markets = self.market_service.all()
    market_dtos = [MarketDTO.from_model(market) for market in markets]
    return Response([market.to_dict() for market in market_dtos])

  def retrieve(self, request, pk=None):
    market = self.market_service.get_by_id(pk)
    if market:
      market_dto = MarketDTO.from_model(market)
      return Response(market_dto.to_dict())
    return Response({"error": "Market not found"}, status=404)

  def create(self, request):
    market_dto = MarketDTO(name=request.data.get('name'))
    added_market = self.market_service.add(market_dto)
    return Response(added_market.to_dict(), status=201)

  def update(self, request, pk=None):
    market_dto = MarketDTO(id=pk, name=request.data.get('name'))
    updated_market = self.market_service.update(market_dto)
    return Response(updated_market.to_dict())

  def destroy(self, request, pk=None):
    market_dto = MarketDTO(id=pk)
    success = self.market_service.delete(market_dto)
    if success:
      return Response({"message": "Market deleted"}, status=204)
    return Response({"error": "Market not found"}, status=404)
