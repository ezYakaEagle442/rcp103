
# Interface
from abc import ABC, abstractmethod
import datetime

from .IEvent import IEvent

class IScheduler(ABC):
    @abstractmethod
    def add_event(self, event: IEvent):
        pass

    @abstractmethod
    def get_event(self):
        pass

    @abstractmethod
    def get_current_time(self):
        pass

    @abstractmethod
    def has_events(self):
        pass

    '''
    @abstractmethod
    def foo(x: int, y: int):
        pass
    '''