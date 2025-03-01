from abc import ABC, abstractmethod
from typing import List
from api.dto.Supplier_dto import SupplierDTO

class SupplierServiceInterface(ABC):

  @abstractmethod
  def get_by_id(self, supplier_id: int) -> SupplierDTO:
    pass

  @abstractmethod
  def all(self) -> List[SupplierDTO]:
    pass

  @abstractmethod
  def add(self, supplier_dto: SupplierDTO) -> SupplierDTO:
    pass

  @abstractmethod
  def update(self, supplier_dto: SupplierDTO) -> SupplierDTO:
    pass

  @abstractmethod
  def delete(self, supplier_dto: SupplierDTO) -> bool:
    pass
