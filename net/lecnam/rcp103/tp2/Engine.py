#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/Engine.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.Engine
# sous Windows/PowerShell: python Engine.py

from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.SchedulerImpl import SchedulerImpl
from net.lecnam.rcp103.tp2.IScheduler import IScheduler
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.ServerImpl import ServerImpl
from net.lecnam.rcp103.tp2.ClientImpl import ClientImpl
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
from net.lecnam.rcp103.tp2.Poisson import Poisson
from net.lecnam.rcp103.tp2.Poisson import Distribution
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl

import numpy as np

import logging
import logging.config
import os
import platform
import string
import sys

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

class Engine:

    nb_clients: int
    nb_servers: int
    lambda_arrival_rate: list
    service_rate: int
    simulation_time: float
    clients: list
    servers: list[IServer]
    scheduler: IScheduler
    queue: IQueue

    def __init__(self):
        logger.debug("+++ Engine : START __init__ ...")
        self.scheduler = SchedulerImpl()
        self.nb_clients = 0
        self.nb_servers = 0
        self.service_rate = 8
        self.lambda_arrival_rate = [4, 6, 8 , 12] # arrival rate (lambda) of the Poisson distribution
        self.simulation_time = 10.0
        self.clients = []
        self.servers = []
        self.queue = QueueImpl()

        logger.debug("+++ Engine : START __init__ ...")

    def create_clients(self, n):
        logger.debug("+++ Engine : START create_clients ...")
        self.nb_clients = n
        self.clients = []

        for i in range(1, n + 1):
            client = ClientImpl(arrival_rate=self.lambda_arrival_rate[i])
            client.set_client_id(i)
            client.set_destination(self.servers[0])
            self.clients.append(client)
            pretty_client = client.print_client()
            logger.debug("+++ Engine : Clients créés :" + str(pretty_client))



        logger.debug("+++ Engine : END create_clients ...")
        
    def create_servers(self, n):
        logger.debug("+++ Engine : START create_servers ...")
        self.nb_servers = n
        logger.debug("+++ Engine : START about to create n servers, n=" + str(n))
        self.servers = []
        for i in range(1, n + 1):
            srv = ServerImpl(server_id=i, mu=self.service_rate, queue=self.queue)
            self.servers.append(srv)
            pretty_srv = srv.print_server()
            logger.debug("+++ Engine : Server created:" + str(pretty_srv))

        logger.debug("+++ Engine : END create_servers ...")

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
        logger.debug("+++ Engine : START run_tests ...")
        # self.test_message()
        # self.test_event()
        # self.test_scheduler()
        self.run_simulationMM1()
        
        print("\n--- RUN SIMULATION ---")
        #self.run()
        logger.debug("+++ Engine : END run_tests ...")

    def run_simulationMM1(self):
        logger.debug("+++ Engine : START run_simulationMM1 ...")
        # dans l'Engine

        L: float
        W: float
        rho: float

        # Iterate on servers and trigget listen() method to process messages in the queue
        for server in self.servers:
            server.listen()

        logger.debug("+++ Engine : END run_simulationMM1 ...")

    def calcul_MM1_rate(self):
        logger.debug("+++ Engine : START calcul_MM1_rate ...")
        print("\n--- TRACE ---")
        print(f"{'Lambda'} \t \t {'Rho'} \t \t {'L'} \t \t {'W'}")

        # Iterate lambda_arrival_rate and calculate L, W, rho for each lambda and print the results 
        for lam in self.lambda_arrival_rate:
            rho = lam / self.service_rate
            try:
                # self.lambda_arrival_rate = [4, 6, 8 , 12] 
                L = rho / (1 - rho)
                W = 1 / (self.service_rate - lam)
                print(f"{lam:<8.3f} \t {rho:<8.3f} \t {L:<8.3f} \t{W:<8.3f}")
            except ZeroDivisionError as e:
                print(f"{lam:<8.3f} \t {rho:<8.3f} \t {"INFINI"} \t {"INFINI"}")
                logger.error("Division by zero error in calcul_MM1_rate")
        print("-" * 45)
        logger.debug("+++ Engine : END calcul_MM1_rate ...")

if __name__ == "__main__":
    engine = Engine()
    engine.create_servers(2)
    engine.create_clients(1)

    cfg = ConfigImpl()
    seed = cfg.get_seed()
    rng = np.random.default_rng(seed=seed)
    
    engine.calcul_MM1_rate()

    # Loop on each client to send a message to the server
    i=1
    ts = 0.0
    for client in engine.clients:
        # MessageImpl(self, message_id, source, destination, timestamp=0.0)
        msg = MessageImpl(i, client.get_client_id(), client.get_destination(), ts+0.10)
        msg.print_message()
        fish = Poisson(rng=rng, lam=client.get_arrival_rate())
        for _ in range(5):
            inter_arrival_time = fish.generate(1)[0] / 1000.0 # Convert ms to seconds
            ts += inter_arrival_time
            msg.set_timestamp(ts)
            client.send_message(msg)
            i+=1

    engine.run_tests()