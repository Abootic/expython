from api.models.order import Order
from typing import List
from abc import ABC, abstractmethod

class OrderRepositoryInterface:

  @abstractmethod
  def get_by_id(self, order_id: int) -> Order:
    pass

  @abstractmethod
  def all(self) -> List[Order]:
    pass

  @abstractmethod
  def add(self, order: Order) -> Order:
    pass

  @abstractmethod
  def update(self, order: Order) -> Order:
    pass

  @abstractmethod
  def delete(self, order: Order) -> Order:
    pass