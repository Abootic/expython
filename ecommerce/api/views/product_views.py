from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from api.dto.product_dto import ProductDTO
from api.factories.service_factory import get_service_factory
from api.services.interfaces.IproductService import IProductService



class ProductViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)  # Add this to allow file uploads

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        service_factory = get_service_factory()
        self.product_service = service_factory.create_product_service(singleton=True)
        self.upload_service = service_factory.create_upload_file_service(singleton=True) # Inject or create an instance of UplaodFileService

    def list(self, request):
        """
        Retrieve a list of all products.
        """
        res = self.product_service.all()
        if res.status.succeeded:
            return Response([obj.to_dict() for obj in res.data], status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific product by ID.
        """
        res = self.product_service.get_by_id(pk)
        if res.status.succeeded:
            return Response(res.data.to_dict(), status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    def create(self, request):
        """
        Create a new product, including handling file upload.
        """
        try:
            # Handle image upload if the image is included in the request
            image = request.FILES.get('image')  # 'image' should match the form field name
            image_path = None
            if image:
                image_path = self.upload_service.upload_file_as_base64(image, 'products')

            # Create ProductDTO and assign the uploaded image path if available
            product_dto = ProductDTO(
                name=request.data.get('name'),
                price=request.data.get('price'),
                supplier_id=request.data.get('supplier_id'),
                image=image_path  # Store the file path or name
            )

            res = self.product_service.add(product_dto)
            if res.status.succeeded:
                return Response({"message": res.status.message}, status=201)
            return Response({"error": res.status.message}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def update(self, request, pk=None):
        """
        Update an existing product.
        """
        try:
            image = request.FILES.get('image')  # Check for image in request
            image_path = None
            if image:
                image_path = self.upload_service.upload_file_as_base64(image, 'products')

            # Create ProductDTO for updating
            product_dto = ProductDTO(
                id=pk,
                name=request.data.get('name'),
                price=request.data.get('price'),
                supplier_id=request.data.get('supplier_id'),
                image=image_path  # Store the file path or name if updated
            )
            res = self.product_service.update(product_dto)
            if res.status.succeeded:
                return Response(res.data.to_dict(), status=res.status.code)
            return Response({"error": res.status.message}, status=res.status.code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def destroy(self, request, pk=None):
        """
        Delete an existing product.
        """
        try:
            product_dto = ProductDTO(id=pk)
            success = self.product_service.delete(product_dto)
            if success:
                return Response({"message": "Product deleted successfully"}, status=204)
            return Response({"error": "Product not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
