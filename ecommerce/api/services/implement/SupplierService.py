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
import string

class SupplierService(SupplierServiceInterface):
    def __init__(self, supplier_repository, userrepoaitory):  # Ensure the parameter name is userrepoaitory
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

    def all(self) -> ResultT:
        try:
            suppliers = self.supplier_repository.all()
            if suppliers:
                supplier_dtos = SupplierMapper.to_dto_list(suppliers)
                return ConcreteResultT.success(supplier_dtos)
            else:
                return ConcreteResultT.fail("No suppliers found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving suppliers: {str(e)}", 500)

    def add(self, supplier_dto: SupplierDTO) -> ResultT:
        try:
            # Ensure user_dto is converted into UserDTO object if it's not already
            user_dto = supplier_dto.user_dto
            if isinstance(user_dto, dict):
                user_dto = UserDTO(**user_dto)  # Convert dict to UserDTO

            # Generate supplier code
            supplier_dto.code = _generate_supplier_code()

            # Check if supplier code already exists
            if self.supplier_repository.exists_by_code(supplier_dto.code):
                return ConcreteResultT.fail("Supplier code already exists", 400)

            # Create user model from the validated and mapped DTO
            user_model = User(
                username=user_dto.username,
                user_type=user_dto.user_type,
                email=user_dto.email,  # Include the email if needed,
                


            )

            # Create the user in the database
            user = self.userrepoaitory.create(user_model,user_dto.password  )

            # Create supplier model (mapping from the DTO)
            supplier_model = Supplier(
                user=user,
                code=supplier_dto.code,
                market_id=supplier_dto.market_id
            )

            # Save the supplier
            supplier = self.supplier_repository.add(supplier_model)

            # Return success result with the created supplier
            return ConcreteResultT.success("aupplier add successfully")

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to add supplier: {str(e)}", 500)

    def update(self, supplier_dto: SupplierDTO) -> ResultT:
        try:
            if not supplier_dto.code:
                supplier_dto.code = _generate_supplier_code()

            # Convert DTO to model and update it
            obj = SupplierMapper.to_model(supplier_dto)
            updated_supplier = self.supplier_repository.update(obj)

            # Return success with updated supplier DTO
            return ConcreteResultT.success(SupplierMapper.to_dto(updated_supplier))

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update supplier: {str(e)}", 500)

    def delete(self, entityDto: SupplierDTO) -> ResultT:
        try:
            # Use the repository to find and delete the supplier
            supplier = self.supplier_repository.get_by_id(entityDto.id)
            if supplier:
                if self.supplier_repository.delete(supplier):
                    return ConcreteResultT.success("Supplier successfully deleted", 200)
                return ConcreteResultT.fail("Failed to delete supplier", 400)
            return ConcreteResultT.fail("Supplier not found", 404)

        except Supplier.DoesNotExist:
            return ConcreteResultT.fail("Supplier not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)


def _generate_supplier_code() -> str:
    SUPPLIER_CODE_PREFIX = "SUP"
    SUPPLIER_CODE_LENGTH = 5
    SUPPLIER_CODE_TOTAL_LENGTH = 8
    random_code = ''.join(random.choices(string.digits, k=SUPPLIER_CODE_LENGTH))
    supplier_code = f"{SUPPLIER_CODE_PREFIX}{random_code}"
    
    if len(supplier_code) > SUPPLIER_CODE_TOTAL_LENGTH:
        raise ValueError(f"Generated supplier code exceeds the maximum length of {SUPPLIER_CODE_TOTAL_LENGTH} characters.")

    return supplier_code
