from abc import ABC, abstractmethod


class BaseNode(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def display(self, identation: int = 0) -> None:
        pass

    @abstractmethod
    def generate_code(self) -> str:
        pass
