from typing import Optional
from .user_dto import UserDTO
from datetime import datetime

class SupplierDTO:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        market_id: Optional[int] = None,
        code: Optional[str] = None,
        user_dto: UserDTO = None,
        join_date: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.market_id = market_id
        self.code = code  # Removed the comma here
        self.user_dto = user_dto  # Removed the comma here
        self.join_date = join_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "market_id": self.market_id,
            "code": self.code,
            "user_dto": self.user_dto,  # Make sure this is serialized properly if it's an object
            "join_date": self.join_date
        }

    def __str__(self) -> str:
        return f"SupplierDTO(id={self.id}, user_id={self.user_id}, market_id={self.market_id}, code={self.code})"
