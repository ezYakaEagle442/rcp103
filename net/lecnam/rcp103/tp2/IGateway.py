
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
    def get_queue() -> IQueue:
        pass

    @abstractmethod
    def set_queue(q: IQueue):
        pass

    @abstractmethod
    def get_server() -> IServer:
        pass
    
    @abstractmethod
    def set_server(server: IServer):
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''