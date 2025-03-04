from api.repositories.interface.percentageRepositoryInterface import PercentageRepositoryInterface
from api.models.percentage import Percentage
from typing import List

class PercentageRepository(PercentageRepositoryInterface):
  def __init__(self):
        self.model = Percentage  
  def get_by_id(self, Percentage_id: int) -> Percentage:
    try:
      return Percentage.objects.get(id=Percentage_id)
    except Percentage.DoesNotExist:
      return None

  def all(self) -> List[Percentage]:
    return Percentage.objects.all()

  def add(self, Percentage: Percentage) -> Percentage:
    if Percentage.pk is None:
      Percentage.save()
      return Percentage
    else:
      raise ValueError("Percentage already exists. Use update Percentage to update an existing Percentage.")

  def update(self, Percentage: Percentage) -> Percentage:
    if Percentage.pk is not None:
      Percentage.save()
      return Percentage
    else:
      raise ValueError("Percentage does not exist. Use add Percentage to add a new Percentage.")

  def delete(self, Percentage: Percentage) -> bool:
    if Percentage:
      Percentage.delete()
      return True
    return False
  def exists_by_code(self, code: str) -> bool:
        # Check if a Percentage with the given code exists
        return self.model.objects.filter(code=code).exists()
  def get_by_supplier(self, supplier_id: int):
    try:
        # Query the database for the percentage record for the given supplier
        return Percentage.objects.filter(supplier_id=supplier_id).first()
    except Exception as e:
        # Log the error or handle it as appropriate
        return None
