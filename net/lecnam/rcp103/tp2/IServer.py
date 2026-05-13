
# Interface
from abc import ABC, abstractmethod

from net.lecnam.rcp103.tp2 import IQueue
from net.lecnam.rcp103.tp2 import IMessage

class IServer(ABC):
        
    @abstractmethod
    def get_queue() -> IQueue:
        pass

    @abstractmethod
    def set_queue(queue: IQueue):
        pass

    @abstractmethod
    def get_server_id():
        pass

    @abstractmethod
    def set_server_id(server_id: int):
        pass

    @abstractmethod 
    def print_server():
        pass
    
    @abstractmethod
    def listen():
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''