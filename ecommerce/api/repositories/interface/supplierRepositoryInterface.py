from abc import ABC, abstractmethod
from typing import List
from api.models.supplier import Supplier

class SupplierRepositoryInterface(ABC):

	@abstractmethod
	def get_by_id(self, supplier_id: int) -> Supplier:
		pass

	@abstractmethod
	def all(self) -> List[Supplier]:
		pass

	@abstractmethod
	def add(self, supplier: Supplier) -> Supplier:
		pass

	@abstractmethod
	def update(self, supplier: Supplier) -> Supplier:
		pass

	@abstractmethod
	def delete(self, supplier: Supplier) -> bool:
		pass
	@abstractmethod
	def exists_by_code(self, code: str) -> bool:
		pass
