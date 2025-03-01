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


class MessageResult:
    def __init__(self, message, code, succeeded):
        self.message = message
        self.code = code
        self.succeeded = succeeded

class ConcreteResultT(ResultT):
    def __init__(self, status, data):
        super().__init__(status, data)

    @classmethod
    def success(cls, data):
        status = MessageResult("Success", 200, True)
        return cls(status, data)

    @classmethod
    def fail(cls, message, code):
        status = MessageResult(message, code, False)
        return cls(status, None)
