from api.Mapper.PercentageMapper import PercentageMapper

from api.repositories.interface.percentageRepositoryInterface import PercentageRepositoryInterface
from api.services.interface.PercentageServiceInterface import PercentageServiceInterface
from api.dto.percentage_dto import PercentageDTO
from api.models.percentage import Percentage
from api.wrpper.Result import ConcreteResultT, ResultT
import json




class PercentageService(PercentageServiceInterface):
    def __init__(self, percentage_repository :PercentageRepositoryInterface):  # Ensure the parameter name is userrepoaitory
        self.percentage_repository = percentage_repository


    

    def get_by_id(self, id: int) -> ResultT:
        try:
            percentage = self.percentage_repository.get_by_id(id)
            if percentage:
                dto = PercentageMapper.to_dto(percentage)
                return ConcreteResultT.success(dto)
            else:
                return ConcreteResultT.fail("Customer not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving percntage: {str(e)}", 500)


    def all(self) -> ResultT:
        try:
            percntage = self.percentage_repository.all()  # Get all customers
            # print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
            # v=PercentageMapper.to_dto(percntage)
            # json_str =json.dumps(v.__dict__)
            # print(json_str)  #

            if percntage:
                dto=PercentageMapper.to_dto_list(percntage)
                return ConcreteResultT.success(dto)
            
            return  ConcreteResultT.fail("percntage not retrive is empty,",200)

        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving percntage: {str(e)}", 500)

    # def add(self, percntage_dto: PercentageDTO) -> ResultT:
    #             try:
    #                model=PercentageMapper.to_model(percntage_dto)
    #                existing_percentage = self.percentage_repository.get_by_supplier(model.supplier_id)
    #                if existing_percentage:
    #                    return ConcreteResultT.fail("suppliers already exsit", 400)

    #                res= self.percentage_repository.add(model)
    #                if(res):
    #                      return ConcreteResultT.success("Percentage added successfully")
                   
    #                return ConcreteResultT.fail("Failed to add Percentage:" )

    #             except Exception as e:
    #                 return ConcreteResultT.fail(f"Failed to add Percentage: {str(e)}", 500)
    def add(self, percentage_dto: PercentageDTO) -> ResultT:
        try:
            # Convert DTO to model
            model = PercentageMapper.to_model(percentage_dto)

            # Check if the supplier already has a percentage
            existing_percentage = self.percentage_repository.get_by_supplier(model.supplier_id)
            if existing_percentage:
                # Return failure if supplier already exists
                return ConcreteResultT.fail("Supplier already exists with a percentage", 400)

            # Add the new percentage
            res = self.percentage_repository.add(model)
            if res:
                return ConcreteResultT.success("Percentage added successfully,")
            
            return ConcreteResultT.fail("Failed to add Percentage", 500)

        except Exception as e:
            # Handle any exceptions
            return ConcreteResultT.fail(f"Failed to add Percentage: {str(e)}", 500)


    def update(self, percntage_dto: PercentageDTO) -> ResultT:
        try:
                   model=PercentageMapper.to_model(percntage_dto)
                   res= self.percentage_repository.update(model)
                   if(res):
                         return ConcreteResultT.success("Percentage update successfully")
                   
                   return ConcreteResultT.fail("Failed to add Percentage:" )

        except Exception as e:
                    return ConcreteResultT.fail(f"Failed to add update: {str(e)}", 500)


    def delete(self, entityDto: PercentageDTO) -> ResultT:
        try:
            # Use the repository to find and delete the Customer
            model = self.percentage_repository.get_by_id(entityDto.id)
            if model:
                if self.percentage_repository.delete(model):
                    return ConcreteResultT.success("percntage successfully deleted", 200)
                return ConcreteResultT.fail("Failed to delete model", 400)
            return ConcreteResultT.fail("percntage not found", 404)

        except model.DoesNotExist:
            return ConcreteResultT.fail("percntage not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)
        
    def assign_percentage_value_to_suppliers(self,market_id: int)-> ResultT:
        try:
            # Use the repository to find and delete the Customer
            model = self.percentage_repository.assign_percentage_value_to_suppliers(market_id)
            if model==1:
                
                    return ConcreteResultT.fail("already assgin percentage value", 200)
            elif  model==2:
              return ConcreteResultT.success(" assgin  percentage value to supplier succesfully")
            else :
                  return ConcreteResultT.fail("something error ", 200)

           
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)
        

        

    



