from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.percentage_dto import PercentageDTO
from api.factories.service_factory import create_Percentage_service
from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action



class PercentageViewSet(viewsets.ViewSet):
  required_roles = ['ADMIN']  # Define roles allowed for this view

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._service = create_Percentage_service()
  @permission_required_for_action({
        'create': [IsAuthenticated, RoleRequiredPermission],
        'list': [IsAuthenticated, RoleRequiredPermission],
        'retrieve': [IsAuthenticated, RoleRequiredPermission],
        'update': [IsAuthenticated, RoleRequiredPermission],
        'destroy': [IsAuthenticated, RoleRequiredPermission]
     })
  def list(self, request):
      res = self._service.all()
      if res.status.succeeded:
            return Response([obj.__dict__  for obj in res.data], status=res.status.code)
      return Response({"error": res.status.message}, status=res.status.code)

  def retrieve(self, request, pk=None):
      res = self._service.get_by_id(pk)
        
      if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)

      return Response({"error": res.status.message}, status=res.status.code)
  def create(self, request):
    try:
        # Creating the ProductDTO from the request data

        percnatge_dto = PercentageDTO(
            supplier_id=request.data.get('supplier_id'),
            market_id=request.data.get('market_id'),
            priority=request.data.get('priority'),
            percentage_value=request.data.get('percentage_value')
        )

        # Call the add method of the service to add the product
        res = self._service.add(percnatge_dto)
        if res.status.succeeded:
            return Response(res.status.message, status=201)

        # Ensure the response is a dictionary, so it's serializable
        return Response(res.status.message, status=201)  # Assuming res.data is a ProductDTO
    except Exception as e:
        # Handle any exception that occurs during the process
        return Response({"error": str(e)}, status=500)




  def update(self, request, pk=None):
     
       update = PercentageDTO( 
            id=pk,
                supplier_id=request.data.get('supplier_id'),
                market_id=request.data.get('market_id'),
                priority=request.data.get('priority'),
                percentage_value=request.data.get('percentage_value')
            )
     
       res=self._service.update(update)
       if res.status.succeeded:
           

            return Response(res.status.message, status=res.status.code)
       return Response({"error": res.status.message}, status=res.status.code)

  def destroy(self, request, pk=None):
    product_dto = PercentageDTO(id=pk)
    success = self._service.delete(product_dto)
    if success:
        return Response(success.status.message, status=204)
    return Response(success.status.message, status=404)
  @action(detail=False, methods=['POST'], url_path='assign_percentage_value_to_suppliers/(?P<market_id>\d+)')
    
  def assign_percentage_value_to_suppliers(self, request, market_id=None):
    
    success = self._service.assign_percentage_value_to_suppliers(market_id)
    if success:
        return Response(success.status.message, status=204)
    return Response(success.status.message, status=404)
