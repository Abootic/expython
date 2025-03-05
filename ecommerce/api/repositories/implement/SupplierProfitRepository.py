from api.models.supplierProfit import SupplierProfit
from api.repositories.interface.SupplierProfitRepositoryInterface import SupplierProfitRepositoryInterface

class SupplierProfitRepositoryImpl(SupplierProfitRepositoryInterface):

         def update_or_create_profit(self, market_id: int, month, profit: float):
                """
                Update or create a SupplierProfit entry for a given market and month.
                """
                supplier_profit, created = SupplierProfit.objects.update_or_create(
                    market_id=market_id,
                    month=month,
                    defaults={'profit': profit}
                )

                if not created:
                    # If the record exists, update the profit
                    supplier_profit.profit += profit
                    supplier_profit.save()

                return supplier_profit