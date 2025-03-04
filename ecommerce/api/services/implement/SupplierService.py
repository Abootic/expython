from api.Mapper.user_mapper import UserMapper
from api.dto.user_dto import UserDTO
from api.models.user import User
from api.repositories.interface.supplierRepositoryInterface import SupplierRepositoryInterface
from api.repositories.interface.userRepositoryInterface import UserRepositoryInterface
from api.services.interface.SupplierServiceInterface import SupplierServiceInterface
from api.dto.Supplier_dto import SupplierDTO
from api.models.supplier import Supplier
from typing import List
from api.Mapper.SupplierMapper import SupplierMapper
from api.wrpper.Result import ConcreteResultT, ResultT
import random
import string,json

class SupplierService(SupplierServiceInterface):
    def __init__(self, supplier_repository:SupplierRepositoryInterface, userrepoaitory:UserRepositoryInterface):  # Ensure the parameter name is userrepoaitory
        self.supplier_repository = supplier_repository
        self.userrepoaitory = userrepoaitory

   

    def get_by_id(self, supplier_id: int) -> ResultT:
        try:
            supplier = self.supplier_repository.get_by_id(supplier_id)
            if supplier:
                supplier_dto = SupplierMapper.to_dto(supplier)
                return ConcreteResultT.success(supplier_dto)
            else:
                return ConcreteResultT.fail("Supplier not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving supplier: {str(e)}", 500)

   

    def all(self) -> List[SupplierDTO]:
        try:
            suppliers = self.supplier_repository.all()  # Get all suppliers
            supplier_dtos = []  # Initialize list for DTOs

            for supplier in suppliers:
                # Ensure the associated user exists for this supplier
                user = supplier.user  # Assuming you have a related field like 'user' in Supplier
                if user:
                    user_dto = UserMapper.to_dto(user)  # Map User to UserDTO
                else:
                    user_dto = None  # Or create an empty UserDTO if no user is found

                # Map Supplier to SupplierDTO, including the user_dto
                supplier_dto = SupplierMapper.to_dto(supplier, user_dto)
                supplier_dtos.append(supplier_dto)

            return ConcreteResultT.success(supplier_dtos)

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to retrieve suppliers: {str(e)}", 500)




    def _generate_supplier_code(self) -> str:
        SUPPLIER_CODE_PREFIX = "SUP"
        SUPPLIER_CODE_LENGTH = 5
        SUPPLIER_CODE_TOTAL_LENGTH = 8

        # Generate random code
        random_code = ''.join(random.choices(string.digits, k=SUPPLIER_CODE_LENGTH))
        supplier_code = f"{SUPPLIER_CODE_PREFIX}{random_code}"

        # Ensure the generated code has the correct length
        if len(supplier_code) != SUPPLIER_CODE_TOTAL_LENGTH:
            raise ValueError(f"Generated supplier code must have {SUPPLIER_CODE_TOTAL_LENGTH} characters.")

        return supplier_code
    def add(self, supplier_dto: SupplierDTO) -> ResultT:
        print("33333333333333333333333333333333333333333333333333333333333333333333333")
        
        # Convert code to string if it's a tuple
        if isinstance(supplier_dto.code, tuple):
            supplier_dto.code = supplier_dto.code[0]  # Take the first element if it's a tuple

        json_str = json.dumps(supplier_dto.to_dict(), default=str)
        print(json_str)
        
        try:
            # Ensure user_dto is converted into UserDTO object if it's not already
            user_dto = supplier_dto.user_dto
            if not user_dto:
                return ConcreteResultT.fail("User DTO is None", 400)

            if isinstance(user_dto, dict):
                user_dto = UserDTO(**user_dto)  # Convert dict to UserDTO

            # Ensure user_dto has required fields
            if not user_dto.username:
                return ConcreteResultT.fail("User DTO missing required field (username)", 400)
            if not user_dto.email:
                return ConcreteResultT.fail("User DTO missing required field (email)", 400)

            # Generate supplier code
            supplier_dto.code = self._generate_supplier_code()
            print("444444444444444444444444444444444444444444444444444444444444444444444444")

            if not supplier_dto.code:  # Ensure code is not None or empty
                return ConcreteResultT.fail("Supplier code is None or empty", 400)
            print("5555555555555555555555555555555")

            # Check if supplier code already exists
            if self.supplier_repository.exists_by_code(supplier_dto.code):
                return ConcreteResultT.fail("Supplier code already exists", 400)
            print("66666666666666666666666666666666")


            # Check if the number of suppliers for the given market exceeds the limit (10 suppliers)
            existing_supplier_count = self.supplier_repository.count_by_market_id(supplier_dto.market_id)
            if existing_supplier_count >= 10:
                return ConcreteResultT.fail("Market already has the maximum number of suppliers (10)", 400)
            print("7777777777777777777777777777")

            # Create user model from the validated and mapped DTO
            user_model = User(
                username=user_dto.username,
                user_type=user_dto.user_type,
                email=user_dto.email,
            
            )
            print(f"supplier_dto.code: {supplier_dto.code}")
            print(f"user_dto.username: {user_dto.username}")
            print(f"user_dto.email: {user_dto.email}")
            print(f"user_dto.user_type: {user_dto.user_type}")

            # Create the user in the database
            user = self.userrepoaitory.create(user_model, user_dto.password)
            if not user:
                return ConcreteResultT.fail("Failed to create user", 500)
            print("8888888888888888888888888888888")

            # # Create supplier model (mapping from the DTO)
            # print(f"supplier.code: {supplier_dto.code}")
            # print(f"user_dto.username: {user_model.username}")
            # print(f"user_dto.email: {user_model.email}")
            # print(f"user_dto.id: {user_model.id}")


            supplier_model = Supplier(
                user=user,
                code=supplier_dto.code,
                market_id=supplier_dto.market_id
            )

            # Save the supplier
            supplier = self.supplier_repository.add(supplier_model)
            if supplier:
                # Return success result with the created supplier
                return ConcreteResultT.success("Supplier added successfully")
            return ConcreteResultT.fail("Failed to create Supplier", 500)

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to add supplier: {str(e)}", 500)



    def update(self, supplier_dto: SupplierDTO) -> ResultT:
        try:
            print("======================================================")
            print(supplier_dto.code)
            # Retrieve the existing supplier from the repository
            supplier = self.supplier_repository.get_by_id(supplier_dto.id)
            if not supplier:
                return ConcreteResultT.fail("Supplier not found", 404)

            # Check if user_dto exists and update the associated user
            if supplier_dto.user_dto:
                user_model = self.userrepoaitory.get_by_id(supplier_dto.user_id)
                if user_model:
                    # Update user fields from user_dto
                    user_model.username = supplier_dto.user_dto.username
                    user_model.email = supplier_dto.user_dto.email
                    user_model.user_type = supplier_dto.user_dto.user_type
                    self.userrepoaitory.update(user_model)
                else:
                    return ConcreteResultT.fail("User not found", 404)

            # Update supplier fields
            supplier.code = supplier_dto.code or supplier.code
            print("suuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
            print(supplier.code)
            if isinstance(supplier.code , tuple):
                supplier.code  = supplier.code[0]

            self.supplier_repository.update(supplier)

            # Return the updated supplier DTO
            updated_supplier_dto = SupplierMapper.to_dto(supplier)
            return ConcreteResultT.success(updated_supplier_dto)

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update supplier: {str(e)}", 500)

    def delete(self, entityDto: SupplierDTO) -> ResultT:
        try:
            # Use the repository to find and delete the supplier
            supplier = self.supplier_repository.get_by_id(entityDto.id)
            if supplier:
                if self.supplier_repository.delete(supplier):
                    # Pass only the message and return a dictionary with status and data
                    return ConcreteResultT.success({"message": "Supplier successfully deleted", "status_code": 200})
                return ConcreteResultT.fail("Failed to delete supplier", 400)
            return ConcreteResultT.fail("Supplier not found", 404)

        except Supplier.DoesNotExist:
            return ConcreteResultT.fail("Supplier not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)

    def count_by_market_id(self, marketid):
        try:
            # Assuming this returns the number of suppliers for a market
            supplier_count = self.supplier_repository.count_by_market_id(marketid)

            if supplier_count is not None:
                # Return the count directly (since it's an integer, no need for DTO mapping)
                 return ConcreteResultT.success(supplier_count)
            else:
                return ConcreteResultT.fail("No suppliers found in this market", 404)

        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving suppliers: {str(e)}", 500)




    
