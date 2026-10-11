from abc import ABC, abstractmethod


class Persona(ABC):

    @property
    @abstractmethod
    def persona(self) -> str:
        pass

    @property
    @abstractmethod
    def style(self) -> str:
        pass

    @property
    @abstractmethod
    def behaviour(self) -> str:
        pass

    @property
    @abstractmethod
    def tools(self) -> str:
        pass
