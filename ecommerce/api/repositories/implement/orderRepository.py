from api.repositories.interface.orderRepositoryInterface import OrderRepositoryInterface
from api.models.order import Order
from typing import List, Optional

class OrderRepository(OrderRepositoryInterface):

  def get_by_id(self, order_id: int) -> Optional[Order]:
    try:
      return Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return None

  def all(self) -> List[Order]:
    return Order.objects.all()

  def add(self, order: Order) -> Order:
    if order.pk is None:
      order.save()
      return order
    else:
      raise ValueError("Order already exists. Use update order to update an existing order.")

  def update(self, order: Order) -> Order:
    if order.pk is not None:
      order.save()
      return order
    else:
      raise ValueError("Order must exist to update.")  

  def delete(self, order: Order) -> bool:
    if order and order.pk is not None:
      order.delete()
      return True
    return False
