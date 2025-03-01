from api.models.supplier import Supplier
from api.dto.Supplier_dto import SupplierDTO

class SupplierMapper:
    @staticmethod
    def to_model(dto: SupplierDTO) -> Supplier:
        return Supplier(
            user_id=dto.user_id,   # Directly assign foreign key ID
            market_id=dto.market_id,
            code=dto.code
        )

    @staticmethod
    def to_dto(supplier: Supplier) -> SupplierDTO:
        return SupplierDTO(
            id=supplier.id,
            user_id=supplier.user_id,  # Use `user_id` directly (no need to access user object)
            market_id=supplier.market_id,
            code=supplier.code
        )
