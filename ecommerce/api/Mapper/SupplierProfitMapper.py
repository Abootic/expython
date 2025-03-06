from api.dto.supplierProfit_dto import SupplierProfitDTO  # Import DTO class
from api.Mapper.SupplierMapper import SupplierMapper  # Import Supplier DTO
from api.models.supplierProfit import SupplierProfit  # Import SupplierProfit model if needed

class SupplierProfitMapper:
    @staticmethod
    def from_model(supplier_profit):
        """
        Convert a SupplierProfit model instance to a SupplierProfitDTO.
        """
        # Directly map model fields to DTO fields
        supplier_dto = SupplierMapper.from_model(supplier_profit.supplier)  # Assuming `SupplierDTO.from_model()` is defined
        return SupplierProfitDTO(
            supplier=supplier_dto,  # Convert the supplier model to a SupplierDTO
            month=supplier_profit.month,
            profit=supplier_profit.profit
        )
    
    @staticmethod
    def to_dict(supplier_profit_dto):
        """
        Convert a SupplierProfitDTO instance to a dictionary representation.
        """
        return supplier_profit_dto.to_dict()
    
    @staticmethod
    def from_dto(supplier_profit_dto):
        """
        Convert a SupplierProfitDTO to a SupplierProfit model instance.
        """
        return SupplierProfit(
            supplier=supplier_profit_dto.supplier.to_model(),  # Assuming `to_model` is defined in SupplierDTO
            month=supplier_profit_dto.month,
            profit=supplier_profit_dto.profit
        )
