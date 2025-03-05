from django.db.models import Sum
from api.models import Product, Percentage
from api.services.interface.SupplierProfitServiceInterface import SupplierProfitServiceInterface
from api.repositories.interface.SupplierProfitRepositoryInterface import SupplierProfitRepositoryInterface

class SupplierProfitServiceImpl(SupplierProfitServiceInterface):
    def __init__(self, repository:SupplierProfitRepositoryInterface):
        self._repository = repository

   
    def update_or_create_profit(self, market_id, month):
        print("111111111111111111111111111111111111111111111111111111111111111111111111" )
        print(f"market_id   {market_id}" )
        print(f"month   {month}" )
        """
        Calculate and save the profit for each supplier in a market for a given month.
        """
        # Step 1: Calculate total market income for the month
        total_income = Product.objects.filter(
            supplier__market__id=market_id  # Traverse Product -> Supplier -> Market
        ).aggregate(total_income=Sum('price'))['total_income'] or 0.0
        
        
        print("222222222222222222222222222222222222222222222222222222222222")
        print(f"total_income   {total_income}" )
       
        supplier_percentages = Percentage.objects.filter(
            supplier__market__id=market_id  # Traverse Percentage -> Supplier -> Market
        )
        print("33333333333333333333333333333333333333333333333333333333")

        for sp in supplier_percentages:
         supplier_profit = (total_income * sp.percentage_value) / 100  # ✅ Calculate profit

        # ✅ Pass supplier, month, and calculated profit
        self._repository.update_or_create_profit(
            supplier=sp.supplier,  # Pass the supplier object
            month=month,           # Pass the month
            profit=supplier_profit # Pass the calculated profit
        )
        return f"Profit calculation completed for market {market_id} for {month}."
