from api.dto.user_dto import UserDTO
from api.models.user import User
from api.repositories.interface.customerRepositoryInterface import CustomerRepositoryInterface
from api.repositories.interface.userRepositoryInterface import UserRepositoryInterface
from api.services.interface.customerServiceInterface import CustomerServiceInterface
from api.dto.customer_dto import CustomerDTO
from api.models.customer import Customer
from typing import List
from api.Mapper.CustomerMapper import CustomerMapper
from api.wrpper.Result import ConcreteResultT, ResultT
import random
import string

class CustomerService(CustomerServiceInterface):
    def __init__(self, customer_repository, user_repository):  # Ensure the parameter name is userrepoaitory
        self.customer_repository = customer_repository
        self.user_repository = user_repository

    def get_by_id(self, Customer_id: int) -> ResultT:
        try:
            Customer = self.customer_repository.get_by_id(Customer_id)
            if Customer:
                Customer_dto = CustomerMapper.to_dto(Customer)
                return ConcreteResultT.success(Customer_dto)
            else:
                return ConcreteResultT.fail("Customer not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving Customer: {str(e)}", 500)

    def all(self) -> ResultT:
        try:
            Customers = self.customer_repository.all()
            if Customers:
                Customer_dtos = CustomerMapper.to_dto_list(Customers)
                return ConcreteResultT.success(Customer_dtos)
            else:
                return ConcreteResultT.fail("No Customers found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving Customers: {str(e)}", 500)

    def add(self, customer_dto: CustomerDTO) -> ResultT:
        try:
            # Ensure user_dto is converted into UserDTO object if it's not already
            user_dto = customer_dto.user_dto
            if isinstance(user_dto, dict):
                user_dto = UserDTO(**user_dto)  # Convert dict to UserDTO

            # Generate supplier code
            customer_dto.code = _generate_Customer_code()

            # Check if supplier code already exists
            if self.customer_repository.exists_by_code(customer_dto.code):
                return ConcreteResultT.fail("Customer code already exists", 400)

            # Create user model from the validated and mapped DTO
            user_model = User(
                username=user_dto.username,
                user_type=user_dto.user_type,
                email=user_dto.email,  # Include the email if needed,
            )

            # Create the user in the database using UserRepository
            user = self.user_repository.create(user_model, user_dto.password)  # Make sure `create` exists here

            # Create customer model (mapping from the DTO)
            customer_model = Customer(
                user=user,
                code=customer_dto.code,
            )

            # Save the customer to the repository
            customer = self.customer_repository.add(customer_model)

            # Return success result with the created customer
            return ConcreteResultT.success("Customer added successfully")

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to add customer: {str(e)}", 500)

    def update(self, Customer_dto: CustomerDTO) -> ResultT:
        try:
            if not Customer_dto.code:
                Customer_dto.code = _generate_Customer_code()

            # Convert DTO to model and update it
            obj = CustomerMapper.to_model(Customer_dto)
            updated_Customer = self.customer_repository.update(obj)

            # Return success with updated Customer DTO
            return ConcreteResultT.success(CustomerMapper.to_dto(updated_Customer))

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update Customer: {str(e)}", 500)

    def delete(self, entityDto: CustomerDTO) -> ResultT:
        try:
            # Use the repository to find and delete the Customer
            Customer = self.customer_repository.get_by_id(entityDto.id)
            if Customer:
                if self.customer_repository.delete(Customer):
                    return ConcreteResultT.success("Customer successfully deleted", 200)
                return ConcreteResultT.fail("Failed to delete Customer", 400)
            return ConcreteResultT.fail("Customer not found", 404)

        except Customer.DoesNotExist:
            return ConcreteResultT.fail("Customer not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)


def _generate_Customer_code() -> str:
    Customer_CODE_PREFIX = "SUP"
    Customer_CODE_LENGTH = 5
    Customer_CODE_TOTAL_LENGTH = 8
    random_code = ''.join(random.choices(string.digits, k=Customer_CODE_LENGTH))
    Customer_code = f"{Customer_CODE_PREFIX}{random_code}"
    
    if len(Customer_code) > Customer_CODE_TOTAL_LENGTH:
        raise ValueError(f"Generated Customer code exceeds the maximum length of {Customer_CODE_TOTAL_LENGTH} characters.")

    return Customer_code
