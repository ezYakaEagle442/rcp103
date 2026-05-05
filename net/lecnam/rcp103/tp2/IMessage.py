
# Interface
from abc import ABC, abstractmethod


class IMessage(ABC):

    @abstractmethod
    def getSource():
        pass

    @abstractmethod
    def getDestination():
        pass

    @abstractmethod
    def getMessageID():
        pass

    @abstractmethod
    def setSource(src: int):
        pass

    @abstractmethod
    def setDestination(dst: int):
        pass

    @abstractmethod
    def setMessageID(msg_id: int):
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''