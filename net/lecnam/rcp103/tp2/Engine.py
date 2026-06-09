#!/usr/bin/python3

# Commande pour lancer le programme :
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/Engine.py
# to debug in WSL2: PYTHONPATH=. python3 -m pdb -m net/lecnam/rcp103/tp2/Engine

# Slide 16
# src = client
# dst = 0 (gateway), 
# node = composant de l'archi: client=1, gateway=0, server=1, server2=2, etc.

from time import sleep

from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.tp2.EventType import EventType
from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.EventImpl import EventImpl
from net.lecnam.rcp103.tp2.SchedulerImpl import SchedulerImpl
from net.lecnam.rcp103.tp2.IScheduler import IScheduler
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.ClientImpl import ClientImpl
from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.ServerImpl import ServerImpl
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
from net.lecnam.rcp103.tp2.GatewayImpl import GatewayImpl
from net.lecnam.rcp103.tp2.IGateway import IGateway

from net.lecnam.rcp103.tp2.Poisson import Poisson, Distribution
from net.lecnam.rcp103.tp2.Exponentielle import Exponentielle


from collections import deque # pour implémenter une queue thread-safe avec FIFO
import matplotlib.pyplot as plt
import sys

import threading
import numpy as np
import logging
import logging.config
import os

config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)
logger = logging.getLogger(__name__)

logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('__main__').setLevel(logging.ERROR)

GATEWAY_ID: int = 0

class Engine:

    nb_clients: int
    nb_servers: int
    lambda_arrival_rate: list
    service_rate: int
    simulation_time: float
    clients: list[IClient]
    servers: list[IServer]
    gateway: IGateway
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
        self.messages_in_queue = 0       # nombre instantané dans la queue
        self.messages_in_system = 0      # nombre instantané dans le système
        self.sum_messages_in_system = 0  # pour calculer la moyenne
        self.sum_waiting_time = 0        # pour le temps d'attente moyen
        self.last_event_time = 0.0       # temps du dernier événement
        self.send_times = {}             # timestamp d'envoi par msgID
        self._rng = np.random.default_rng(seed=ConfigImpl().get_seed())
        self.nb_servers = 1
        self.busy_servers = 0
        self.waiting_queue = []
        self.max_queue_size = -1  # -1 = infini
        self.dropped_count = 0
        self.max_in_system = 0
        self.max_in_queue = 0
        logger.debug("+++ Engine : END __init__")
        self.dropped_count = 0

    def create_gateway(self, max_queue_size, nb_servers):
        self.max_queue_size = max_queue_size
        self.nb_servers = nb_servers
        logger.debug(f"+++ Engine : START create_gateway with max_queue_size={max_queue_size}, nb_servers={nb_servers}")
        gateway_queue = QueueImpl(max_size=max_queue_size)
        self.gateway = GatewayImpl(queue=gateway_queue, nb_servers=nb_servers)
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
        self.max_in_system = max(self.max_in_system, self.messages_in_system)
        self.max_in_queue = max(self.max_in_queue, len(self.waiting_queue))
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
            dst = GATEWAY_ID
            self.total_messages += 1
            self.messages_in_queue += 1

        elif event_type == "RECV_MSG":
            node = GATEWAY_ID
            event_name = "RECV"
            dst = GATEWAY_ID
            self.messages_in_queue -= 1
            self.messages_in_system += 1
            self.send_times[msg.get_message_id()] = t

            if self.busy_servers < self.nb_servers:
                self.busy_servers += 1
                service_time = self._rng.exponential(1.0 / self.service_rate)
                t_dept = t + service_time
                e_dept = EventImpl(msg.get_message_id() + 100, msg, "MSG_DEPT", t_dept)
                self.scheduler.add_event(e_dept)
            else:
                # vérifier la capacité K
                if self.max_queue_size > 0 and len(self.waiting_queue) >= self.max_queue_size:
                    # DROP
                    self.dropped_count += 1
                    self.messages_in_system -= 1
                else:
                    self.waiting_queue.append(msg)

        elif event_type == "MSG_DEPT":
            node = GATEWAY_ID
            event_name = "DEPT"
            dst = GATEWAY_ID
            self.messages_in_system -= 1
            send_t = self.send_times.get(msg.get_message_id(), t)
            self.sum_waiting_time += (t - send_t)
            logger.debug(f"+++ Engine : MSG_DEPT traité pour msg {msg.get_message_id()} | W={t - send_t:.4f}")

            if self.waiting_queue:
                next_msg = self.waiting_queue.pop(0)
                service_time = self._rng.exponential(1.0 / self.service_rate)
                t_dept = t + service_time
                e_dept = EventImpl(next_msg.get_message_id() + 100, next_msg, "MSG_DEPT", t_dept)
                self.scheduler.add_event(e_dept)
                logger.debug(f"+++ Engine : MSG_DEPT chaîné pour msg {next_msg.get_message_id()} @ t={t_dept:.4f}")
            else:
                self.busy_servers -= 1
                logger.debug(f"+++ Engine : serveur libéré | busy_servers={self.busy_servers}")
                ''' 
                # Slide 16
                # src = client
                # dst = 0 (gateway),
                # node = composant de l'archi: client=1, gateway=0, server=1, server2=2, etc.
                # '''
        print(
                f"{t:<8.4f} "
                f"{node:<5} "
                f"{event_name:<6} "
                f"{msg.get_source():<5} "
                f"{dst:<5} "
                f"{msg.get_message_id():<5}"
            )

    def run(self):
        logging.disable(logging.DEBUG)  # ← désactiver DEBUG pendant la trace
        #self.print_trace_header()
        while self.scheduler.has_events():
            event = self.scheduler.get_event()
            self.generate_trace(event)
        logging.disable(logging.NOTSET)  # ← réactiver après
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

    def calcul_MM1_rate(self,lam):
        rho = lam / self.service_rate
        print(f"\n--- Métriques théoriques M/M/1 (lam={lam}) ---")
        print(f"{'Lambda':<10} {'Rho':<10} {'L':<10} {'W':<10}")
        print("-" * 45)
        if lam >= self.service_rate:
            print(f"{lam:<10.3f} {rho:<10.3f} {'INFINI':<10} {'INFINI':<10}")
        else:
            L = rho / (1 - rho)
            W = 1 / (self.service_rate - lam)
            print(f"{lam:<10.3f} {rho:<10.3f} {L:<10.3f} {W:<10.3f}")
        print("-" * 45)

    def run_tests(self):
        logger.debug("+++ Engine : START run_tests")
        self.run()                # ← affiche la trace
        # self.run_simulationMM1()  # ← démarre les threads serveurs
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
        print(f"Messages droppés           : {self.dropped_count}")
        print(f"Max messages dans le système : {self.max_in_system}")
        print(f"Max messages dans la queue   : {self.max_in_queue}")

    def get_metrics(self):
        t_total = self.last_event_time
        L = self.sum_messages_in_system / t_total if t_total > 0 else 0
        W = self.sum_waiting_time / self.total_messages if self.total_messages > 0 else 0
        return L, W
    
if __name__ == "__main__":

    # 1. INPUTS AVANT de rediriger stdout (pour que l'user voit la console)
    L_sim = []
    W_sim = []

    mm1k = int(input("Pécisez 4|8 pour M/M/1/K, M/M/1/4 — file limitée à 4 | M/M/1/8 — file limitée à 8: ").strip())

    nb_clients = int(input("Nombre de clients : ").strip())
    nb_servers = int(input("Nombre de serveurs : ").strip())

    engine = Engine()
    engine.create_gateway(max_queue_size=mm1k, nb_servers=nb_servers)

    # 2. Rediriger stdout vers un fichier APRÈS les inputs
    with open('simulation_output.log', 'w') as f:
        original_stdout = sys.stdout
        sys.stdout = f

        if mm1k == -1:
            model_name = f"M/M/{nb_servers} — file infinie"
        else:
            model_name = f"M/M/{nb_servers}/{mm1k}"

        for lam in [4, 6, 8, 12]:
            print(f"\n=== Simulation lambda={lam} ===")
            logger.debug("+++ Engine : Main START")

            # Architecture :
            # client (id>=1) -> SEND -> gateway (id=0) -> RECV -> queue -> DEPT -> server (id>=1)
            logger.debug(f"+++ Engine : nb_clients={nb_clients}, nb_servers={nb_servers}")

            ### SI ON VEUT UNE QUEUE A FILE LIMITEE : 
            # M/M/1/4 — file limitée à 4
            # M/M/1/8 — file limitée à 8        
            logger.info(f"+++ Engine : M/M/1/K={mm1k}")

            logger.debug("+++ Engine : Engine instantiated, about to trigger servers to listen ...")
            # engine.run_simulationMM1()  # GateWayImpl.init démarre les threads serveurs
            logger.debug("+++ Engine : Engine instantiated, now Servers are listening.")
            
            engine.create_clients(nb_clients) # clients pointent vers la gateway

            cfg = ConfigImpl()
            seed = cfg.get_seed()
            rng = np.random.default_rng(seed=seed)

            engine.calcul_MM1_rate(lam)

            # Génération des messages : chaque client envoie vers la gateway (dst=0)
            engine.print_trace_header()
            i = 1
            ts = 0.0

            # 1. Générer les événements SEND, RECV, DEPT pour chaque message
            for client in engine.clients:
                ts = 0.0
                # inter-arrival times selon une loi exponentielle de paramètre lambda
                fish = Poisson(rng=rng, lam=lam)
                #fish = Exponentielle(rng=rng, scale=1.0/lam)
                for _ in range(100):     ## ATTENTION A MODIFIER METTRE UN GROS NOMBRE POUR LES METRIQUES
                    inter_arrival = fish.generate(1)[0]
                    ts += inter_arrival
                    msg = MessageImpl(i, client.get_client_id(), GATEWAY_ID, ts)
                    t_send = ts
                    t_recv = ts + 1.0 # EN slide 10:latence de transmission client->gateway es tde 1s
                
                    e_send = EventImpl(i*3,   msg, "SEND_MSG", t_send)
                    e_recv = EventImpl(i*3+1, msg, "RECV_MSG", t_recv)
                    
                    # 2. Enregistrer les événements dans le scheduler 
                    engine.scheduler.add_event(e_send)
                    engine.scheduler.add_event(e_recv)
                    
                    i += 1

            logger.info(f"+++ Engine : {engine.scheduler.count_events()} messages générés et événements programmés dans le scheduler")

            engine.run_tests()
            L, W = engine.get_metrics()
            L_sim.append(L)
            W_sim.append(W)

            logger.debug("+++ Engine : Main END")

        # Restaurer stdout à la fin du with (hors de la boucle for)
        sys.stdout = original_stdout

    lambdas = [4, 6, 8, 12]
    L_theo = [1.0, 3.0]
    W_theo = [0.25, 0.75]
    lambdas_theo = [4, 6]  # seulement pour λ<μ
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(lambdas, L_sim, 'b-o', label='L simulé')
    plt.plot(lambdas_theo, L_theo, 'r--o', label='L théorique')
    plt.xlabel('λ (msg/s)')
    plt.ylabel('L')
    plt.title('Nombre moyen dans le système')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(lambdas, W_sim, 'b-o', label='W simulé')
    plt.plot(lambdas_theo, W_theo, 'r--o', label='W théorique')
    plt.xlabel('λ (msg/s)')
    plt.ylabel('W (s)')
    plt.title('Temps moyen dans le système')
    plt.legend()
    plt.grid(True)

    plt.suptitle(f'{model_name} — Simulé vs Théorique')
    plt.tight_layout()
    plt.savefig('resultats_MM1.png')
    plt.show()