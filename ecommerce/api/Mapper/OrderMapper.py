from api.models.order import Order
from api.dto.order_dto import OrderDTO
from decimal import Decimal

class OrderMapper:
    
    @staticmethod
    def to_model(order_dto: OrderDTO) -> Order:
        """
        Convert OrderDTO to Order model instance.
        """
        return Order(
            id=order_dto.id,
            customer_id=order_dto.customer_id,
            product_id=order_dto.product_id,
            total_price=Decimal(order_dto.total_price),  # Ensure price is a Decimal
            price=Decimal(order_dto.price),  # Ensure price is a Decimal
            create_at=order_dto.create_at,  # Assuming the date is passed as string in 'YYYY-MM-DD'
            quantity=order_dto.quantity
        )
    
    @staticmethod
    def from_model(order: Order) -> OrderDTO:
        """
        Convert Order model instance to OrderDTO.
        """
        return OrderDTO(
            id=order.id,
            customer_id=order.customer.id if order.customer else None,
            product_id=order.product.id if order.product else None,
            total_price=order.total_price,
            price=order.price,
            create_at=order.create_at.strftime('%Y-%m-%d'),  # Adjust the date format as needed
            quantity=order.quantity
        )
