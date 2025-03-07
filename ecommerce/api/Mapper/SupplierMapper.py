from django.apps import apps
from api.dto.Supplier_dto import SupplierDTO

class SupplierMapper:

    @staticmethod
    def to_model(supplier_dto: SupplierDTO):
        """Convert SupplierDTO to Supplier model."""
        Supplier = apps.get_model('api', 'Supplier')
        return Supplier(
            code=supplier_dto.code,
            market_id=supplier_dto.market_id,
            join_date=supplier_dto.join_date
            # Add other fields if necessary
        )

    @staticmethod
    def to_dto(supplier, user_dto=None) -> SupplierDTO:
        """Convert Supplier model to SupplierDTO."""
        return SupplierDTO(
            id=supplier.id,
            code=supplier.code,
            market_id=supplier.market_id,
            user_dto=user_dto.to_dict() if user_dto else None,
            join_date=supplier.join_date
        )

    @staticmethod
    def to_dto_list(suppliers: list, user_dto=None) -> list:
        """Convert a list of Supplier models to a list of SupplierDTOs."""
        # Ensure that suppliers is a list
        return [SupplierMapper.to_dto(supplier, user_dto) for supplier in suppliers]