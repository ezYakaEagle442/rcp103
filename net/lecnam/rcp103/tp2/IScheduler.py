
# Interface
from abc import ABC, abstractmethod
import datetime

from rcp103.net.lecnam.rcp103.tp2 import IEvent


class IScheduler(ABC):

    @abstractmethod
    def getCurrentTime():
        pass

    @abstractmethod
    def getEvent():
        pass

    @abstractmethod
    def setCurrentTime(src: datetime):
        pass

    @abstractmethod
    def setEvent(evt: IEvent):
        pass

    @abstractmethod
    def addEvent(evt: IEvent):
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''