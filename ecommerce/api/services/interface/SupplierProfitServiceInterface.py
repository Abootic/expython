from abc import ABC, abstractmethod

class SupplierProfitServiceInterface(ABC):
    @abstractmethod
    def calculate_supplier_profit(self, market_id, month):
        pass