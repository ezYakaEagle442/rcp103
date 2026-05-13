
# Interface
from abc import ABC, abstractmethod

from net.lecnam.rcp103.tp2.IServer import IServer

class IMessage(ABC):

    @abstractmethod
    def get_source():
        pass

    @abstractmethod
    def get_destination():
        pass

    @abstractmethod
    def get_message_id():
        pass

    @abstractmethod
    def set_source(src: str):
        pass

    @abstractmethod
    def set_destination(dst: IServer):
        pass

    @abstractmethod
    def set_message_id(msg_id: int):
        pass

    @abstractmethod
    def print_message():
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''