
# Interface
from abc import ABC, abstractmethod

from net.lecnam.rcp103.tp2 import IGateway
from net.lecnam.rcp103.tp2 import IQueue
from net.lecnam.rcp103.tp2 import IServer

class IGateway(ABC):

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def get_queue(self):
        pass

    @abstractmethod
    def set_queue(self, q):
        pass

    @abstractmethod
    def get_servers(self) -> list:
        pass

    @abstractmethod
    def set_servers(self, servers: list):
        pass

    @abstractmethod
    def receive_message(self, msg) -> None:
        """Reçoit un message d'un client, l'enfile et dispatche."""
        pass

    @abstractmethod
    def dispatch(self) -> None:
        """Défile un message et l'envoie au prochain serveur disponible."""
        pass

    @abstractmethod
    def print_gateway(self) -> str:
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''