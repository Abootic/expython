from api.models.percentage import Percentage
from api.dto.percentage_dto import PercentageDTO

class PercentageMapper:
    @staticmethod
    def to_dto(percentage: Percentage) -> PercentageDTO:
        return PercentageDTO(
            supplier_id=percentage.supplier.id if percentage.supplier else None,
            market_id=percentage.market.id if percentage.market else None,
            priority=percentage.priority,
            percentage_value=percentage.percentage_value
        )
    
    @staticmethod
    def to_model(dto: PercentageDTO) -> Percentage:
        return Percentage(
            supplier_id=dto.supplier_id,
            market_id=dto.market_id,
            priority=dto.priority,
            percentage_value=dto.percentage_value
        )