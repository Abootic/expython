from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.Supplier_dto import SupplierDTO
from api.factories.service_factory import create_supplier_service  # Assuming service factory is used

class SupplierViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = create_supplier_service()

    def list(self, request):
        res = self._service.all()
        if res.status.succeeded:
            return Response([supplier.to_dict() for supplier in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def retrieve(self, request, pk=None):
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def create(self, request):
        obj = SupplierDTO(code=request.data.get('code'))
        res = self._service.add(obj)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def update(self, request, pk=None):
        obj = SupplierDTO(id=pk, code=request.data.get('code'))
        res = self._service.update(obj)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def destroy(self, request, pk=None):
        obj = SupplierDTO(id=pk)
        res = self._service.delete(obj)
        if res.status.succeeded:
            return Response({"message": "Supplier deleted"}, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)
