#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/Engine.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.Engine
# sous Windows/PowerShell: python Engine.py

from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.SchedulerImpl import SchedulerImpl


import logging
import logging.config
import os
import platform
import string
import sys

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

class Engine:

    nb_clients: int
    nb_servers: int
    simulation_time: float
    clients: list
    scheduler: SchedulerImpl

    def __init__(self):
        self.scheduler = SchedulerImpl()
        self.nb_clients = 0
        self.nb_servers = 1
        self.simulation_time = 10.0
        self.clients = []

    def create_clients(self, n):
        self.nb_clients = n
        self.clients = []

        for i in range(1, n + 1):
            self.clients.append(i)

        print("Clients créés :", self.clients)

    def print_trace_header(self):
        print("\n--- TRACE ---")
        print(f"{'time':<8} {'node':<5} {'event':<6} {'src':<5} {'dst':<5} {'msgID':<5}")
        print("-" * 45)

    def generate_trace(self, event):
        msg = event.get_message()

        event_type = event.get_event_type()

        if event_type == "SEND_MSG":
            node = msg.get_source()
            event_name = "SEND"
        elif event_type == "RECV_MSG":
            node = 0
            event_name = "RECV"
        elif event_type == "MSG_DEPT":
            node = 0
            event_name = "DEPT"
        else:
            node = 0
            event_name = event_type

        print(
            f"{event.get_event_time():<8.3f} "
            f"{node:<5} "
            f"{event_name:<6} "
            f"{msg.get_source():<5} "
            f"{msg.get_destination():<5} "
            f"{msg.get_message_id():<5}"
        )

    def run(self):
        self.print_trace_header()

        while self.scheduler.has_events():
            event = self.scheduler.get_event()
            self.generate_trace(event)

    def test_message(self):
        print("\n--- TEST MESSAGE ---")
        msg = MessageImpl(1, 1, 0, 0.0)
        msg.print_message()

    def test_event(self):
        print("\n--- TEST EVENT ---")
        msg = MessageImpl(1, 1, 0, 0.0)
        event = EventImpl(1, msg, "SEND_MSG", 1.567)
        prettyEvt = event.print_event()
        print("+++ Pretty print = " + str(prettyEvt))

    def test_scheduler(self):
        print("\n--- TEST SCHEDULER ---")

        msg1 = MessageImpl(1, 1, 0, 0.0)
        msg2 = MessageImpl(2, 3, 0, 0.0)

        e1 = EventImpl(1, msg1, "SEND_MSG", 1.202)
        e2 = EventImpl(2, msg1, "RECV_MSG", 1.916)
        e3 = EventImpl(3, msg2, "SEND_MSG", 2.320)
        e4 = EventImpl(4, msg2, "RECV_MSG", 2.391)
        e5 = EventImpl(5, msg1, "MSG_DEPT", 4.572)
        e6 = EventImpl(6, msg2, "MSG_DEPT", 5.916)

        self.scheduler.add_event(e5)
        self.scheduler.add_event(e1)
        self.scheduler.add_event(e3)
        self.scheduler.add_event(e6)
        self.scheduler.add_event(e2)
        self.scheduler.add_event(e4)

        self.scheduler.print_scheduler()
        logger.debug("+++ Engine : print_scheduler ...")
        logger.info(self.scheduler.print_scheduler())        

    def run_tests(self):
        self.test_message()
        self.test_event()
        self.test_scheduler()

        print("\n--- RUN SIMULATION ---")
        self.run()


if __name__ == "__main__":
    engine = Engine()
    engine.create_clients(3)
    engine.run_tests()