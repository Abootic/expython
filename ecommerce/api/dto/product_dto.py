class ProductDTO:
    def __init__(self, id=None, name=None, price=None, supplier_id=None):
        self.id = id
        self.name = name
        self.price = price
        self.supplier_id = supplier_id

    @classmethod
    def from_model(cls, product):
        # Map fields from the product model to the ProductDTO
        return cls(
            id=product.id,
            name=product.name,
            price=product.price,
            supplier_id=product.supplier_id
        )

    def to_dict(self):
        # Ensure that the returned dictionary is serializable
        return {
            'id': self.id,
            'name': self.name,
            'price': str(self.price),  # Ensure that price is serializable
            'supplier_id': self.supplier_id
        }
