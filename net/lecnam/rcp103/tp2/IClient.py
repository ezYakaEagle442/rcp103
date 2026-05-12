
# Interface
from abc import ABC, abstractmethod

from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.IServer import IServer


class IClient(ABC):

    @abstractmethod
    def get_destination():
        pass

    # Set Queue name
    @abstractmethod
    def set_destination(dst: IServer):
        pass

    @abstractmethod
    def get_arrival_rate():
        pass

    @abstractmethod
    def set_arrival_rate(rate: int):
        pass

    @abstractmethod
    def send_message(msg: IMessage):
        pass

    @abstractmethod
    def print_client():
        pass

    @abstractmethod
    def set_message(msg: IMessage):
        pass

    @abstractmethod
    def get_message(msg: IMessage):
        pass

    @abstractmethod
    def set_client_id(id: int):
        pass

    @abstractmethod
    def get_client_id():
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''