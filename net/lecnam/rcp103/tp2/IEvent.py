# Interface
from abc import ABC, abstractmethod
import datetime
import string


class IEvent(ABC):

    @abstractmethod
    def get_event_time() ->  datetime.datetime:
        pass

    @abstractmethod
    def get_event_type()  ->  string:
        pass

    @abstractmethod
    def set_event_time(evtString: datetime):
        pass

    @abstractmethod
    def set_event_type(evtType: string):
        pass

    @abstractmethod
    def print_event():
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''