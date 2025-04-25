from abc import ABC, abstractmethod


class BaseValidator(ABC):
    @abstractmethod
    def get_func_name(self):
        pass

    @abstractmethod
    def generate_func_body(self) -> str:
        pass
