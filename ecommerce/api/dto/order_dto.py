from datetime import datetime

class OrderDTO:
    def __init__(self, id=None, customer_id=None, product_id=None, total_price=None, price=None, quantity=None, create_at=None):
        self.id = id if id is not None else None  # id is auto-generated (null/None for now)
        self.customer_id = customer_id
        self.product_id = product_id
        self.total_price = total_price
        self.price = price
        self.quantity = quantity
        self.create_at = create_at if create_at else datetime.now()  # Automatically set the current date/time

    # Example of adding a to_dict method to convert DTO to dict
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "total_price": str(self.total_price),
            "price": str(self.price),
            "quantity": self.quantity,
            "create_at": self.create_at.isoformat()
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
