from typing import Optional
from api.models.customer import Customer

class CustomerDTO:
  def __init__(self, id: Optional[int] = None, user_id: Optional[int] = None, phone_number: Optional[str] = None, code: Optional[str] = None):
    self.id = id
    self.user_id = user_id
    self.phone_number = phone_number
    self.code = code

  @classmethod
  def from_model(cls, customer: Customer) -> 'CustomerDTO':
    return cls(
      id=customer.id,
      user_id=customer.user.id if customer.user else None,
      phone_number=customer.phone_number,
      code=customer.code
    )

  def to_dict(self) -> dict:
    return {
      'id': self.id,
      'user_id': self.user_id,
      'phone_number': self.phone_number,
      'code': self.code
    }

  def __str__(self) -> str:
    return f"CustomerDTO(id={self.id}, user_id={self.user_id}, phone_number={self.phone_number}, code={self.code})"
