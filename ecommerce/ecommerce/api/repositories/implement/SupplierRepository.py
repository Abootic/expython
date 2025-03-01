from api.repositories.interface.supplierRepositoryInterface import SupplierRepositoryInterface
from api.models.supplier import Supplier
from typing import List

class SupplierRepository(SupplierRepositoryInterface):

  def get_by_id(self, supplier_id: int) -> Supplier:
    try:
      return Supplier.objects.get(id=supplier_id)
    except Supplier.DoesNotExist:
      return None

  def all(self) -> List[Supplier]:
    return Supplier.objects.all()

  def add(self, supplier: Supplier) -> Supplier:
    if supplier.pk is None:
      supplier.save()
      return supplier
    else:
      raise ValueError("supplier already exists. Use update supplier to update an existing supplier.")

  def update(self, supplier: Supplier) -> Supplier:
    if supplier.pk is not None:
      supplier.save()
      return supplier
    else:
      raise ValueError("supplier does not exist. Use add supplier to add a new supplier.")

  def delete(self, supplier: Supplier) -> bool:
    if supplier:
      supplier.delete()
      return True
    return False
