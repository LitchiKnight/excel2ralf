from abc import ABC, abstractmethod

class RalBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def gen_ralf_code(self) -> str:
        """Generate RALF code for the derived class."""
        pass