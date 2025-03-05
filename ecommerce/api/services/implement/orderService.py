from django.utils import timezone
from api.Mapper.OrderMapper import OrderMapper
from api.dto.order_dto import OrderDTO
from api.models.supplierProfit import SupplierProfit
from api.repositories.interface.orderRepositoryInterface import OrderRepositoryInterface
from api.services.interface.orderServiceInterface import OrderServiceInterface
from typing import List
from api.wrpper.Result import ConcreteResultT, ResultT

class OrderService(OrderServiceInterface):

    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def get_by_id(self, order_id: int) -> ResultT:
        try:
            order = self.order_repository.get_by_id(order_id)
            if order:
                dto = OrderMapper.convert_to_dto(order)
                return ConcreteResultT.success(dto)
            else:
                return ConcreteResultT.fail("Order not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving order: {str(e)}", 500)

    def all(self) -> ResultT:
        try:
            orders = self.order_repository.all()
            if orders:
                order_dtos = [OrderMapper.convert_to_dto(order) for order in orders]
                return ConcreteResultT.success(order_dtos)
            else:
                return ConcreteResultT.fail("No orders found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving orders: {str(e)}", 500)

    def add(self, order: OrderDTO) -> ResultT:
        try:
            order_model = OrderMapper.convert_to_model(order)
            added_order = self.order_repository.add(order_model)
            return ConcreteResultT.success(OrderMapper.convert_to_dto(added_order))
        except Exception as e:
            return ConcreteResultT.fail(f"Error adding order: {str(e)}", 500)

    def update(self, order: OrderDTO) -> ResultT:
        try:
            order_model = OrderMapper.convert_to_model(order)
            updated_order = self.order_repository.update(order_model)
            return ConcreteResultT.success(OrderMapper.convert_to_dto(updated_order))
        except Exception as e:
            return ConcreteResultT.fail(f"Error updating order: {str(e)}", 500)

    def delete(self, order: OrderDTO) -> ResultT:
        try:
            order_model = OrderMapper.convert_to_model(order)
            self.order_repository.delete(order_model)
            return ConcreteResultT.success("Order deleted successfully")
        except Exception as e:
                return ConcreteResultT.fail(f"Error deleting order: {str(e)}", 500)
    def update_order_and_profit(self, order_id: int, new_price: float, new_quantity: int) -> ResultT:
            """
            Update the order price and quantity, and recalculate the supplier profit based on new values.
            """
            try:
                # Get the order using the repository
                order = self.order_repository.get_by_id(order_id)
                if not order:
                    return ConcreteResultT.fail("Order not found", 404)

                # Update the order with the new price and quantity
                order.price = new_price
                order.quantity = new_quantity
                order.save()

                # Calculate the new profit based on updated price and quantity
                order_profit = new_price * new_quantity

                # Get the supplier associated with the product in the order
                supplier = self.order_repository.get_supplier_by_product(order.product)
                if not supplier:
                    return ConcreteResultT.fail("Supplier not found", 404)

                # Update or create the supplier's profit record (recalculate the profit)
                self.order_repository.update_or_create_supplier_profit(supplier, order_profit)

                return ConcreteResultT.success("Order and profit updated successfully")
            except Exception as e:
                return ConcreteResultT.fail(f"Error updating order and profit: {str(e)}", 500)

    def process_order(self, order_id: int) -> ResultT:
            try:
                result = self.calculate_supplier_profit(order_id)
                if result.is_success():
                    return ConcreteResultT.success("Order processed successfully")
                return result
            except Exception as e:
                return ConcreteResultT.fail(f"Error processing order: {str(e)}", 500)

    def get_supplier_profit_for_month(self, supplier_id: int, month: int) -> ResultT:
        try:
            profit = self.order_repository.get_supplier_profit_for_month(supplier_id, month)
            if profit is not None:
                return ConcreteResultT.success(profit)
            else:
                return ConcreteResultT.fail("No profit found for this supplier in the given month", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving supplier profit: {str(e)}", 500)
