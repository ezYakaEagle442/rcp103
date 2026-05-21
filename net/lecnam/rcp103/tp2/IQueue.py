
# Interface
from abc import ABC, abstractmethod

from net.lecnam.rcp103.tp2 import IMessage

class IQueue(ABC):


    @abstractmethod
    def get_queue_size(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def enqueue(msg: IMessage):
        pass

    @abstractmethod
    def dequeue():
        pass

    @abstractmethod
    def count_messages(self):
        pass
    
    @abstractmethod
    def print_messages():
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''