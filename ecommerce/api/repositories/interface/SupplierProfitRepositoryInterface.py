from abc import ABC, abstractmethod
from api.models.supplierProfit import SupplierProfit

class SupplierProfitRepositoryInterface(ABC):
    @abstractmethod
    def update_or_create_profit(self, supplier, month, profit):
        pass