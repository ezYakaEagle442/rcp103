#!/usr/bin/python3

# Commande pour lancer le programme :
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/Engine.py

from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.SchedulerImpl import SchedulerImpl
from net.lecnam.rcp103.tp2.IScheduler import IScheduler
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.ServerImpl import ServerImpl
from net.lecnam.rcp103.tp2.ClientImpl import ClientImpl
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
from net.lecnam.rcp103.tp2.GatewayImpl import GatewayImpl
from net.lecnam.rcp103.tp2.Poisson import Poisson, Distribution
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl

import threading
import numpy as np
import logging
import logging.config
import os

config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)
logger = logging.getLogger(__name__)

GATEWAY_ID: int = 0

class Engine:

    nb_clients: int
    nb_servers: int
    lambda_arrival_rate: list
    service_rate: int
    simulation_time: float
    clients: list[IClient]
    servers: list[IServer]
    gateway: GatewayImpl
    scheduler: IScheduler

    def __init__(self):
        logger.debug("+++ Engine : START __init__")
        self.scheduler = SchedulerImpl()
        self.nb_clients = 0
        self.nb_servers = 0
        self.service_rate = 8
        self.lambda_arrival_rate = [4, 6, 8, 12]
        self.simulation_time = 10.0
        self.clients = []
        self.servers = []
        self.gateway = None
        # Métriques
        self.total_messages = 0          # nombre total de messages
        self.messages_in_system = 0      # nombre instantané dans le système
        self.messages_in_queue = 0       # nombre instantané dans la queue
        self.sum_messages_in_system = 0  # pour calculer la moyenne
        self.sum_waiting_time = 0        # pour le temps d'attente moyen
        self.last_event_time = 0.0       # temps du dernier événement
        self.send_times = {}             # timestamp d'envoi par msgID
        logger.debug("+++ Engine : END __init__")
        

    def create_servers(self, n):
        """Crée n serveurs (id de 1 à n), chacun avec sa propre queue."""
        logger.debug("+++ Engine : START create_servers")
        self.nb_servers = n
        self.servers = []
        for i in range(1, n + 1):
            # Chaque serveur a sa propre queue (pas de queue partagée)
            srv = ServerImpl(server_id=i, mu=self.service_rate)
            self.servers.append(srv)
            logger.info(f"+++ Engine : Server created: {srv.print_server()}")
        logger.debug("+++ Engine : END create_servers")

    def create_gateway(self, max_queue_size: int = -1):
        logger.debug("+++ Engine : START create_gateway")
        gateway_queue = QueueImpl(max_size=max_queue_size)
        self.gateway = GatewayImpl(queue=gateway_queue, servers=self.servers)
        logger.info(f"+++ Engine : Gateway created: {self.gateway.print_gateway()}")
        logger.debug("+++ Engine : END create_gateway")

    def create_clients(self, n):
        """Crée n clients pointant vers la gateway (destination = 0)."""
        logger.debug("+++ Engine : START create_clients")
        self.nb_clients = n
        self.clients = []
        for i in range(1, n + 1):
            rate = self.lambda_arrival_rate[i - 1] if i - 1 < len(self.lambda_arrival_rate) else self.lambda_arrival_rate[-1]
            client = ClientImpl(arrival_rate=rate, gateway=self.gateway)
            client.set_client_id(i)
            self.clients.append(client)
            logger.info(f"+++ Engine : Client created: {client.print_client()}")
        logger.debug("+++ Engine : END create_clients")

    def print_trace_header(self):
        print("\n--- TRACE ---")
        print(f"{'time':<8} {'node':<5} {'event':<6} {'src':<5} {'dst':<5} {'msgID':<5}")
        print("-" * 45)

    def generate_trace(self, event):
        msg = event.get_message()
        event_type = event.get_event_type()
        t = event.get_event_time()

        # Intégration temporelle
        dt = t - self.last_event_time
        self.sum_messages_in_system += self.messages_in_system * dt
        self.last_event_time = t

        if event_type == "SEND_MSG":
            node = msg.get_source()
            event_name = "SEND"
            dst = 0
            self.total_messages += 1
            self.messages_in_system += 1
            self.messages_in_queue += 1
            self.send_times[msg.get_message_id()] = t

        elif event_type == "RECV_MSG":
            node = 0
            event_name = "RECV"
            dst = 0
            self.messages_in_queue -= 1

        elif event_type == "MSG_DEPT":
            node = msg.get_destination()
            event_name = "DEPT"
            dst = msg.get_destination()
            self.messages_in_system -= 1
            send_t = self.send_times.get(msg.get_message_id(), t)
            self.sum_waiting_time += (t - send_t)

        else:
            node = 0
            event_name = event_type
            dst = msg.get_destination()

        logger.info(
            f"{t:<8.4f} "
            f"{node:<5} "
            f"{event_name:<6} "
            f"{msg.get_source():<5} "
            f"{dst:<5} "
            f"{msg.get_message_id():<5}"
        )

    def run(self):
        self.print_trace_header()
        while self.scheduler.has_events():
            event = self.scheduler.get_event()
            self.generate_trace(event)
        self.print_metrics()

    def run_simulationMM1(self):
        """Lance un thread d'écoute par serveur."""
        logger.debug("+++ Engine : START run_simulationMM1")
        threads = []
        for server in self.servers:
            logger.info(f"+++ Engine : starting listener for {server.print_server()}")
            thread = threading.Thread(target=server.listen, daemon=True)
            thread.start()
            threads.append(thread)
        logger.debug("+++ Engine : END run_simulationMM1")

    def calcul_MM1_rate(self):
        print("\n--- Métriques M/M/1 ---")
        print(f"{'Lambda':<10} {'Rho':<10} {'L':<10} {'W':<10}")
        print("-" * 45)
        for lam in self.lambda_arrival_rate:
            rho = lam / self.service_rate
            try:
                L = rho / (1 - rho)
                W = 1 / (self.service_rate - lam)
                print(f"{lam:<10.3f} {rho:<10.3f} {L:<10.3f} {W:<10.3f}")
            except ZeroDivisionError:
                print(f"{lam:<10.3f} {rho:<10.3f} {'INFINI':<10} {'INFINI':<10}")
        print("-" * 45)

    def run_tests(self):
        logger.debug("+++ Engine : START run_tests")
        self.run()                # ← affiche la trace
        self.run_simulationMM1()  # ← démarre les threads serveurs
        logger.debug("+++ Engine : END run_tests")

    def print_metrics(self):
        print("\n--- Métriques simulées ---")
        if self.total_messages == 0:
            print("Aucun message traité.")
            return
        t_total = self.last_event_time
        avg_in_system = self.sum_messages_in_system / t_total if t_total > 0 else 0
        avg_waiting = self.sum_waiting_time / self.total_messages
        dropped = self.gateway.get_queue().get_dropped_messages()
        print(f"Total messages envoyés     : {self.total_messages}")
        print(f"Messages dans le système   : {self.messages_in_system}")
        print(f"Messages dans la queue     : {self.messages_in_queue}")
        print(f"Moyenne dans le système(L) : {avg_in_system:.4f}")
        print(f"Temps d'attente moyen  (W) : {avg_waiting:.4f}")
        dropped = self.gateway.get_queue().get_dropped_messages()
        print(f"Messages droppés           : {dropped}")

if __name__ == "__main__":
    logger.debug("+++ Engine : Main START")

    # Architecture :
    # client (id>=1) -> SEND -> gateway (id=0) -> RECV -> queue -> DEPT -> server (id>=1)

    nb_clients = int(input("Nombre de clients : ").strip())
    nb_servers = int(input("Nombre de serveurs : ").strip())

    logger.debug(f"+++ Engine : nb_clients={nb_clients}, nb_servers={nb_servers}")

    engine = Engine()
    engine.create_servers(nb_servers)   # serveurs créés en premier (la gateway en a besoin)
    #engine.create_gateway()             # gateway créée après les serveurs

    ### SI ON VEUT UNE QUEUE A FILE LIMITEE : 
    engine.create_gateway(max_queue_size=4)             # gateway créée après les serveurs
    # M/M/1/4 — file limitée à 4
    #engine.create_gateway(max_queue_size=4)
    # M/M/1/8 — file limitée à 8
    #engine.create_gateway(max_queue_size=8)
    engine.create_clients(nb_clients)   # clients pointent vers la gateway

    cfg = ConfigImpl()
    seed = cfg.get_seed()
    rng = np.random.default_rng(seed=seed)

    engine.calcul_MM1_rate()

    # Génération des messages : chaque client envoie vers la gateway (dst=0)
    engine.print_trace_header()
    i = 1
    ts = 0.0
    for client in engine.clients:
        fish = Poisson(rng=rng, lam=client.get_arrival_rate())
        for _ in range(50):     ## ATTENTION A MODIFIER METTRE UN GROS NOMBRE POUR LES METRIQUES
            inter_arrival = fish.generate(1)[0] / 1000.0
            ts += inter_arrival
            msg = MessageImpl(i, client.get_client_id(), GATEWAY_ID, ts)
            t_send = ts
            t_recv = ts + 0.10
            t_dept = ts + 0.125
            e_send = EventImpl(i*3-2, msg, "SEND_MSG", t_send)
            e_recv = EventImpl(i*3-1, msg, "RECV_MSG", t_recv)
            e_dept = EventImpl(i*3,   msg, "MSG_DEPT", t_dept)
            engine.scheduler.add_event(e_send)
            engine.scheduler.add_event(e_recv)
            engine.scheduler.add_event(e_dept)
            client.send_message(msg)
            i += 1

    engine.run_tests()
    logger.debug("+++ Engine : Main END")
