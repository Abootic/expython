from typing import Optional

class SupplierDTO:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        market_id: Optional[int] = None,
        code: Optional[str] = None
    ):
        self.id = id
        self.user_id = user_id
        self.market_id = market_id
        self.code = code

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "market_id": self.market_id,
            "code": self.code,
        }

    def __str__(self) -> str:
        return f"SupplierDTO(id={self.id}, user_id={self.user_id}, market_id={self.market_id}, code={self.code})"
