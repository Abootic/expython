from api.models.customer import Customer
from api.dto.user_dto import UserDTO
from api.dto.customer_dto import CustomerDTO

class CustomerMapper:

    @staticmethod
    def to_model(customer_dto: CustomerDTO) -> Customer:
        """Convert CustomerDTO to Customer model."""
        return Customer(
            code=customer_dto.code,
            phone_number=customer_dto.phone_number,
            user_id=customer_dto.user_id
        )

    @staticmethod
    def to_dto(customer: Customer) -> CustomerDTO:
        """Convert Customer model to CustomerDTO."""
        return CustomerDTO(
            id=customer.id,
            user_id=customer.user.id if customer.user else None,
            phone_number=customer.phone_number,
            code=customer.code
        )

    @staticmethod
    def to_dto_list(customers: list) -> list:
        """Convert a list of Customer models to a list of CustomerDTOs."""
        return [CustomerMapper.to_dto(customer) for customer in customers]
