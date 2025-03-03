from api.dto.order_dto import OrderDTO
from typing import List
from abc import ABC, abstractmethod

class OrderServiceInterface(ABC):

  @abstractmethod
  def get_by_id(self, order_dto: int) -> OrderDTO:
    pass

  @abstractmethod
  def all(self) -> List[OrderDTO]:
    pass

  @abstractmethod
  def add(self, order_dto: OrderDTO) -> OrderDTO:
    pass

  @abstractmethod
  def update(self, order_dto: OrderDTO) -> OrderDTO:
    pass

  @abstractmethod
  def delete(self, order_dto: OrderDTO) -> bool:
    pass