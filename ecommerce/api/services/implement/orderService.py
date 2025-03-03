from api.repositories.interface.orderRepositoryInterface import OrderRepositoryInterface
from api.services.interface.orderServiceInterface import OrderServiceInterface
from api.dto.order_dto import OrderDTO
from api.models.order import Order
from typing import List
from api.wrpper.Result import ConcreteResultT, ResultT
from api.Mapper.OrderMapper import OrderMapper  # Assuming you have this mapper

class OrdersService(OrderServiceInterface):

    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def get_by_id(self, order_id: int) -> ResultT:
        try:
            order = self.order_repository.get_by_id(order_id)
            if order:
                # Wrap the OrderDTO in a success result
                return ConcreteResultT.success(OrderDTO.from_model(order))
            return ConcreteResultT.fail("Order not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving order: {str(e)}", 500)

    def all(self) -> ResultT:
        try:
            orders = self.order_repository.all()
            if orders:
                # Wrap a list of OrderDTOs in a success result
                order_dtos = [OrderDTO.from_model(order) for order in orders]
                return ConcreteResultT.success(order_dtos)
            return ConcreteResultT.fail("No orders found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving orders: {str(e)}", 500)

    def add(self, order_dto: OrderDTO) -> ResultT:
        try:
            # # Convert DTO to model
            # order = Order(
            #     id=order_dto.id,
            #     customer_id=order_dto.customer.id,
            #     product_id=order_dto.product.id,
            #     total_price=order_dto.total_price,
            #     quantity=order_dto.quantity
            # )
            order=OrderMapper.to_model(order_dto)
            added_order = self.order_repository.add(order)
            # Wrap the created order DTO in a success result
            return ConcreteResultT.success(OrderDTO.from_model(added_order))
        except Exception as e:
            return ConcreteResultT.fail(f"Failed to add order: {str(e)}", 500)

    def update(self, order_dto: OrderDTO) -> ResultT:
        try:
            # Update the order model
            order = Order(
                id=order_dto.id,
                customer_id=order_dto.customer.id,
                product_id=order_dto.product.id,
                total_price=order_dto.total_price,
                quantity=order_dto.quantity
            )
            updated_order = self.order_repository.update(order)
            # Wrap the updated order DTO in a success result
            return ConcreteResultT.success(OrderDTO.from_model(updated_order))
        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update order: {str(e)}", 500)

    def delete(self, order_dto: OrderDTO) -> ResultT:
        try:
            order = Order.objects.get(id=order_dto.id)
            if self.order_repository.delete(order):
                return ConcreteResultT.success("Order successfully deleted", 200)
            return ConcreteResultT.fail("Failed to delete order", 400)
        except Order.DoesNotExist:
            return ConcreteResultT.fail("Order not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)
