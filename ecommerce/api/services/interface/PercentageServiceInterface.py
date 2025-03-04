from abc import ABC, abstractmethod
from typing import List
from api.dto.percentage_dto import PercentageDTO

class PercentageServiceInterface(ABC):

  @abstractmethod
  def get_by_id(self, customer_id: int) -> PercentageDTO:
    pass

  @abstractmethod
  def all(self) -> List[PercentageDTO]:
    pass

  @abstractmethod
  def add(self, customer_dto: PercentageDTO) -> PercentageDTO:
    pass

  @abstractmethod
  def update(self, supplier_dto: PercentageDTO) -> PercentageDTO:
    pass

  @abstractmethod
  def delete(self, supplier_dto: PercentageDTO) -> bool:
    pass

