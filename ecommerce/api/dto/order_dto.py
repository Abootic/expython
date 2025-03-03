from decimal import Decimal
from typing import Optional

class OrderDTO:
    def __init__(
        self,
        id: int,
        customer_id: Optional[int],  # Optional in case customer is null
        product_id: Optional[int],    # Optional in case product is null
        total_price: Decimal,
        price: Decimal,
        create_at: str,  # You can adjust this based on your date format preferences
        quantity: int
    ):
        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.total_price = total_price
        self.price = price
        self.create_at = create_at
        self.quantity = quantity

    def to_dict(self) -> dict:
        """Convert the DTO to a dictionary."""
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "total_price": str(self.total_price),  # Ensure Decimal is stringified
            "price": str(self.price),
            "create_at": self.create_at,
            "quantity": self.quantity
        }

    @staticmethod
    def from_model(order) -> 'OrderDTO':
        """Convert an Order model to an OrderDTO."""
        return OrderDTO(
            id=order.id,
            customer_id=order.customer.id if order.customer else None,
            product_id=order.product.id if order.product else None,
            total_price=order.total_price,
            price=order.price,
            create_at=order.create_at.strftime('%Y-%m-%d'),  # Adjust as needed
            quantity=order.quantity
        )
