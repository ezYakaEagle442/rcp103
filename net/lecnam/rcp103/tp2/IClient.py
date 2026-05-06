
# Interface
from abc import ABC, abstractmethod

class IClient(ABC):

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
    def set_destination(dst: str):
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