#!/usr/bin/python3
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/EventImplMockTest.py
# Use unittest.mock to create a mock SimulateurImpl for Mock testing
# https://docs.python.org/3/library/unittest.mock.html

import traceback
import logging

from unittest.mock import MagicMock
from net.lecnam.rcp103.tp2.EventImpl import EventImplMockTest

from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.IEvent import IEvent
from .IMessage import IMessage
from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.EventType import EventType

# Create a mock instance of SimulateurImpl
mock_sim = MagicMock(spec=EventImpl)

# Example: set return value for calcul
mock_sim.get_event_time.return_value = 1.42

msg = MessageImpl(1, "Test message", "Alice", "Bob")

# Use the mock in your test
result = mock_sim.get_event_time()

print("Mocked calcul result:", result)  # Output: Mocked calcul result: 1,42

# You can also assert calls
mock_sim.get_event_time.assert_called_with()