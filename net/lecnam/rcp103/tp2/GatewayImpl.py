# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/GatewayImpl.py
#
# #####################################################################


# Slide 16
# src = client
# dst = 0 (gateway), 
# node = composant de l'archi: client=1, gateway=0, server=1, server2=2, etc.

import datetime
import os
import platform
import string
import sys
import secrets
import traceback

import logging
import logging.config
import threading

from net.lecnam.rcp103.tp2.EventType import EventType
from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.ServerImpl import ServerImpl
from net.lecnam.rcp103.tp2.IGateway import IGateway
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.SimulateurException import SimulateurException

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels
# Class d'Implémentation
class GatewayImpl(IGateway):
    """
    Gateway (node id = 0).
    Reçoit les messages des clients, les met en queue
    et les dispatche vers les serveurs disponibles (id >= 1).
    Stratégie de dispatch : round-robin.
    """

    GATEWAY_ID: int = 0

    queue: IQueue
    servers: list[IServer]
    service_rate: int
    _rr_index: int # index round-robin

    def __init__(self, queue: IQueue, nb_servers: int):
        logger.debug("+++ GatewayImpl : START Constructor")
        self._rr_index = 0
        self.service_rate = 8
        self.queue = queue

        logger.debug(f"+++ GatewayImpl : max_queue_size={queue.get_queue_size()}")    
        nb_msg = self.queue.count_messages()
        logger.debug(f"+++ GatewayImpl : current_nb_msg_in_queue={nb_msg}")

        self.create_servers(nb_servers)
        logger.info(f"+++ GatewayImpl : {len(self.servers)} server(s) enregistré(s)")
        logger.debug("+++ GatewayImpl : END Constructor")

    # --- Accesseurs queue ---
    def get_queue(self) -> IQueue:
        return self.queue

    def set_queue(self, queue: IQueue):
        self.queue = queue

    # --- Accesseurs serveurs ---
    def get_servers(self) -> list:
        return self.servers

    def set_servers(self, servers: list):
        self.servers = servers

    def create_servers(self, n):
        """Crée n serveurs (id de 1 à n), chacun lisant dans la même Queue."""
        logger.debug("+++ GatewayImpl : START create_servers")
        self.nb_servers = n
        self.servers = []
        for i in range(1, n + 1):
            srv = ServerImpl(server_id=i, mu=self.service_rate, queue=self.queue)
            self.servers.append(srv)
            logger.info(f"+++ GatewayImpl : Server created: {srv.print_server()}")
        logger.debug("+++ GatewayImpl : END create_servers")

    # Compatibilité ancienne interface (un seul serveur)

    def is_empty(self) -> bool:
        logger.debug("+++ GatewayImpl : START is_empty")
        try:            
            if not self.queue._lock.acquire(timeout=0.1):
                logger.warning("+++ GatewayImpl : Lock non disponible, échec de is_empty")
                return None
            else:
                logger.debug("+++ GatewayImpl : Lock bien disponible !")
                return self.queue.is_empty()
        finally:
            self.queue._lock.release()  # ← ajout
            logger.debug("+++ GatewayImpl : Lock released in is_empty()")
            logger.debug("+++ GatewayImpl : END is_empty")

    def _next_server(self) -> IServer:

        """Sélectionne le prochain serveur en round-robin."""
        logger.debug("+++ GatewayImpl : START _next_server")
        
        if not self.servers:
            raise RuntimeError("GatewayImpl _next_server: aucun serveur enregistré")
        
        with self.queue._lock:  # ← ajout
            srv = self.servers[self._rr_index % len(self.servers)]
            self._rr_index += 1
        
        logger.debug("+++ GatewayImpl : END _next_server")
        return srv

    def receive_message(self, msg: IMessage):
        """
        Appelé par le client : enfile le message (destination = 0 = gateway).
        Génère l'événement RECV côté gateway, puis dispatche vers un serveur.
        """
        logger.debug(f"+++ GatewayImpl receive_message: RECV msg id={msg.get_message_id()} "
                     f"src={msg.get_source()} @ t={msg.get_timestamp():.4f}")

        srv = self._next_server()
        srv_id = srv.get_server_id()
        msg.set_destination(srv_id)

        # Enfile dans la queue partagée
        accepted = self.queue.enqueue(msg)
        if accepted:
            logger.info(f"+++ GatewayImpl receive_message: msg {msg.print_message()} mis en queue "
                        f"(taille={self.queue.count_messages()}) et dispacthé vers SERVER {srv_id} ")
            self.servers[srv_id - 1].set_srv_proc(srv_id) # server_id starts at 1, list index starts at 0
            # self.dispatch(msg)
        else:
            logger.warning(f"+++ GatewayImpl receive_message: msg {msg.get_message_id()} DROPPED")

    def dispatch(self, msg: IMessage):
        logger.debug("+++ GatewayImpl : START dispatch")
        """Défile le premier message et l'envoie au prochain serveur disponible."""
        if self.queue.is_empty():
            logger.debug("+++ GatewayImpl : dispatch appelé mais Queue vide")
            return
        
        srv = self._next_server()
        srv_id = srv.get_server_id()

        # Met à jour la destination dans le message
        msg.set_destination(srv_id)
        self.servers[srv_id - 1].set_srv_proc(srv_id) # server_id starts at 1, list index starts at 0

        logger.debug(f"+++ GatewayImpl : Dispatching msg {msg.get_message_id()} to server id={srv_id} | srv_proc set to {srv_id} ")
        logger.debug("+++ GatewayImpl : END dispatch")

    # --- Affichage ---
    def print_gateway(self):
        logger.debug("+++ GatewayImpl : START print_gateway")
        q_size = self.queue.count_messages()
        srvs = ", ".join(str(s.print_server()) for s in self.servers)
        result = (f"[GATEWAY] ID={self.GATEWAY_ID} | "
                  f"Queue size={q_size} | Servers=[{srvs}]")
        logger.debug(f"+++ GatewayImpl : {result}")
        logger.debug("+++ GatewayImpl : END print_gateway")
        return result

