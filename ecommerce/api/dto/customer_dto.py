from typing import Optional
from .user_dto import UserDTO

class CustomerDTO:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        code: Optional[str] = None,
        user_dto:UserDTO=None
    ):
        self.id = id
        self.user_id = user_id
        self.code = code,
        self.user_dto=user_dto

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "code": self.code,
            "user_dto":self.user_dto
        }

    def __str__(self) -> str:
        return f"CustomerDTO(id={self.id}, user_id={self.user_id},  code={self.code})"
