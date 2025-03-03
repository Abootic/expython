from api.dto.Supplier_dto import SupplierDTO
from api.models.supplier import Supplier


class SupplierMapper:
    
    @staticmethod
    def to_model(supplier_dto: SupplierDTO) -> Supplier:
        """Convert SupplierDTO to Supplier model."""
        return Supplier(
            code=supplier_dto.code,
            market_id=supplier_dto.market_id,
            # You can add other fields from SupplierDTO if necessary
        )

    @staticmethod
    def to_dto(supplier: Supplier, user_dto=None) -> SupplierDTO:
        """Convert Supplier model to SupplierDTO."""
        return SupplierDTO(
            id=supplier.id,
            code=supplier.code,
            market_id=supplier.market_id,
            user_dto=user_dto.to_dict() if user_dto else None  # Convert UserDTO to dict
        )

    @staticmethod
    def to_dto_list(suppliers: list) -> list:
        """Convert a list of Supplier models to a list of SupplierDTOs."""
        return [SupplierMapper.to_dto(supplier) for supplier in suppliers]
