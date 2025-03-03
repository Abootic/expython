from api.dto.customer_dto import CustomerDTO
from api.models.customer import Customer


class CustomerMapper:
    @staticmethod
    def to_dto(customer, user_dto=None):
        # Ensure that user_dto is included if available
        return CustomerDTO(
            id=customer.id,
            code=customer.code,
            user_dto=user_dto  # Adding user DTO to the customer DTO
        )

    # If you need to handle a list of customers
    @staticmethod
    def to_dto_list(customers):
        return [CustomerMapper.to_dto(customer) for customer in customers]
    @staticmethod
    def to_model(customer_dto: CustomerDTO):
        # Convert CustomerDTO back to Customer model for database operations
        return Customer(
            id=customer_dto.id,
            code=customer_dto.code,
            user_id=customer_dto.user_dto.id if customer_dto.user_dto else None  # Assuming user_id is linked in the DTO
        )