from abc import ABC, abstractmethod

class ResultT(ABC):
    def __init__(self, status, data):
        self.status = status
        self.data = data

    @abstractmethod
    def success(cls, data):
        pass

    @abstractmethod
    def fail(cls, message, code):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class MessageResult:
    def __init__(self, message, code, succeeded):
        self.message = message
        self.code = code
        self.succeeded = succeeded


class ConcreteResultT(ResultT):
    def __init__(self, status: MessageResult, data):
        super().__init__(status, data)

    @classmethod
    def success(cls, data, message="success"):
        # Create a success status with a custom message and code 200
        status = MessageResult(message, 200, True)
        return cls(status, data)

    @classmethod
    def fail(cls, message, code):
        # Ensure you pass both the message and the code
        status = MessageResult(message, code, False)
        return cls(status, None)

    def to_dict(self):
        # Convert the status and data into a dictionary format
        return {
            "success": self.status.succeeded,
            "message": self.status.message,
            "data": self.data,
            "status_code": self.status.code
        }
