#!/usr/bin/python3
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/EventImplMockTest.py
# Use unittest.mock to create a mock SimulateurImpl for Mock testing
# https://docs.python.org/3/library/unittest.mock.html

import traceback
import logging

import unittest
from unittest.mock import MagicMock
from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.EventType import EventType

class EventImplMockTest(unittest.TestCase):

    def test_create_class_call_method(self):
        # Create a mock instance of EventImpl
        mock_sim = MagicMock(spec=EventImpl)

        # Example: set return value for calcul
        msg = MessageImpl(1, "Alice", "Bob", 1.64)
        mock_sim.get_message.return_value = msg

        mock_sim.get_event_time.return_value = 1.42
        mock_sim.get_event_type.return_value = "SEND_MSG" # "Fake Foo Event"
        mock_sim.get_event_id.return_value = 42

        # Use the mock in your test
        t = mock_sim.get_event_time()
        type = mock_sim.get_event_type()
        id = mock_sim.get_event_id()

        print("Mocked id:", id)
        print("Mocked type:", type)
        print("Mocked t:", t)

        # You can also assert calls
        mock_sim.get_event_time.assert_called_once()
        self.assertEqual(t, 1.42)
        self.assertEqual(type, "SEND_MSG")
        self.assertEqual(id, 42)

if __name__ == '__main__':
    unittest.main()