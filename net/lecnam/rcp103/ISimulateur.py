
# Interface
from abc import ABC, abstractmethod


class ISimulateur(ABC):
    @abstractmethod
    def calcul(x: int, y: int):
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''