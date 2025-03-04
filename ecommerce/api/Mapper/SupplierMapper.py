from api.dto.Supplier_dto import SupplierDTO
from api.models.supplier import Supplier

class SupplierMapper:

    @staticmethod
    def to_model(supplier_dto: SupplierDTO) -> Supplier:
        """Convert SupplierDTO to Supplier model."""
        return Supplier(
            code=supplier_dto.code,
            market_id=supplier_dto.market_id,
            # Add other fields if necessary
        )

    @staticmethod
    def to_dto(supplier: Supplier, user_dto=None) -> SupplierDTO:
        """Convert Supplier model to SupplierDTO."""
        return SupplierDTO(
            id=supplier.id,
            code=supplier.code,
            market_id=supplier.market_id,
            user_dto=user_dto.to_dict() if user_dto else None  # Convert UserDTO to dict if provided
        )

    @staticmethod
    def to_dto_list(suppliers: list, user_dto=None) -> list:
        """Convert a list of Supplier models to a list of SupplierDTOs."""
        # Ensure that suppliers is a list
        return [SupplierMapper.to_dto(supplier, user_dto) for supplier in suppliers]
