
# Interface
from abc import ABC, abstractmethod
import datetime
import string


class IEvent(ABC):

    @abstractmethod
    def getEventTime() ->  datetime.datetime:
        pass

    @abstractmethod
    def getEventType()  ->  string:
        pass

    @abstractmethod
    def setEventTime(evtString: datetime):
        pass

    @abstractmethod
    def setEventType(evtType: string):
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''
