# Interface
from abc import ABC, abstractmethod
import datetime

from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IScheduler import IScheduler

from collections import deque # pour implémenter une queue thread-safe avec FIFO

class SchedulerImpl(IScheduler):

    events: deque[IEvent]
    current_time: float

    def __init__(self):
        self.events = deque() # Use deque for efficient FIFO
        self.current_time = 0.0

    def add_event(self, event):
        t = event.get_event_time()
        for i, e in enumerate(self.events):
            if (e.get_event_time() > t):
                self.events.insert(i, event)
                return
        self.events.append(event)

    def get_events(self) -> deque[IEvent]:
        return self.events

    def count_events(self) -> int:
        return len(self.events)

    def get_event(self):
        if not self.events:
            return None
        event = self.events.popleft()
        self.current_time = event.get_event_time()
        return event

    def get_current_time(self):
        return self.current_time

    def has_events(self):
        return bool(self.events)
    
    def print_scheduler(self):
        resultat = ""
        for event in self.events:
            resultat += f"Event ID: {event.eventID}, Type: {event.eventType}, Time: {event.eventTime}\n"
        return resultat