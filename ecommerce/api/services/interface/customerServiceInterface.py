from abc import ABC, abstractmethod
from typing import List
from api.dto.customer_dto import CustomerDTO

class CustomerServiceInterface(ABC):

  @abstractmethod
  def get_by_id(self, customer_id: int) -> CustomerDTO:
    pass

  @abstractmethod
  def all(self) -> List[CustomerDTO]:
    pass

  @abstractmethod
  def add(self, customer_dto: CustomerDTO) -> CustomerDTO:
    pass

  @abstractmethod
  def update(self, supplier_dto: CustomerDTO) -> CustomerDTO:
    pass

  @abstractmethod
  def delete(self, supplier_dto: CustomerDTO) -> bool:
    pass

