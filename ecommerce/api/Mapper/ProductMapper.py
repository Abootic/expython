# product_mapper.py
from api.dto.product_dto import ProductDTO
from api.models.product import Product

class ProductMapper:
    @staticmethod
    def from_model(product: Product) -> ProductDTO:
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
    def to_model(product_dto: ProductDTO) -> Product:
        """
        Converts a ProductDTO back to a Product model for database operations.
        """
        # Assuming supplier_id is provided in the DTO and you want to link it back to a supplier model
        return Product(
            id=product_dto.id,
            name=product_dto.name,
            price=product_dto.price,
            supplier_id=product_dto.supplier_id  # Assuming supplier is linked via supplier_id
        )
