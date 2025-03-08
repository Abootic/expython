from django.apps import apps
from api.dto.product_dto import ProductDTO

class ProductMapper:
    @staticmethod
    def from_model(product) -> ProductDTO:
        """
        Converts a Product model instance to a ProductDTO.
        """
        return ProductDTO(
            id=product.id,
            name=product.name,
            price=product.price,
            supplier_id=product.supplier.id if product.supplier else None  # Safely get supplier_id
        )

    @staticmethod
    def from_model_list(products) -> list:
        """
        Converts a list of Product model instances to a list of ProductDTOs.
        """
        return [ProductMapper.from_model(product) for product in products]

    @staticmethod
    def to_model(product_dto: ProductDTO):
        """
        Converts a ProductDTO back to a Product model for database operations.
        """
        Product = apps.get_model('api', 'Product')
        return Product(
            id=product_dto.id,
            name=product_dto.name,
            price=product_dto.price,
            supplier_id=product_dto.supplier_id  # Assuming supplier is linked via supplier_id
        )