# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/ClientImpl.py
#
#####################################################################

from abc import abstractmethod
import datetime
import os
import logging
import logging.config

import numpy as np

from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.EventType import EventType
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.SimulateurException import SimulateurException
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.Poisson import Poisson
from net.lecnam.rcp103.tp2.Poisson import Distribution
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
from net.lecnam.rcp103.tp2.IServer import IServer

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

# Class d'Implémentation
class ClientImpl(IClient):

    GATEWAY_ID: int = 0

    """
    Client qui envoie ses messages vers la gateway (node id = 0).
    Il n'a plus de référence directe à un IServer.
    """

    message: IMessage
    arrival_rate: int # arrival rate (lambda) of the Poisson distribution
    queue: IQueue
    client_id: int
    destination_id: int # toujours 0 = gateway

    def __init__(self, arrival_rate: int, q:IQueue):
        logger.debug(f"+++ ClientImpl : START Constructor")

        seed = cfg.get_seed()
        logger.debug(f"+++ ClientImpl : seed={seed}")
        logger.debug(f"+++ ClientImpl : arrival_rate={arrival_rate}")
        self.arrival_rate = arrival_rate
        self.gateway = gateway
        self.destination_id = 0  # gateway id
        logger.debug(f"+++ ClientImpl : arrival_rate={arrival_rate}, destination=gateway(0)")
        logger.debug("+++ ClientImpl : END Constructor")

    def send_message(self, msg: IMessage):
        """Envoie un message vers la gateway."""
        logger.debug(f"+++ ClientImpl : START send_message id={msg.get_message_id()}")
        # S'assurer que la destination est bien 0 (gateway)
        msg.set_destination(self.GATEWAY_ID)
        self.gateway.receive_message(msg)
        logger.debug(f"+++ ClientImpl : END send_message")

    def set_client_id(self, id: int):
        self.client_id = id

    def get_client_id(self):
        return self.client_id

    def get_destination(self):
        """Retourne l'id de la gateway (0)."""
        return self.destination_id

    def set_destination(self, dst):
        """Accepte un int (node id) ou un objet gateway."""
        if isinstance(dst, int):
            self.destination_id = dst
        else:
            # Si on passe un objet gateway, on stocke la référence
            self.gateway = dst
            self.destination_id = self.GATEWAY_ID
    def get_arrival_rate(self):
        return self.arrival_rate

    def set_arrival_rate(self, rate: int):
        self.arrival_rate = rate

    def set_message(self, msg: IMessage):
        self.message = msg

    def get_message(self):
        return self.message

    # --- Affichage ---
    def print_client(self):
        logger.debug("+++ ClientImpl : START print_client")
        client = (f"[CLIENT] ID={self.client_id} | ArrivalRate={self.arrival_rate} "
                  f"| Destination=gateway(id={self.destination_id})")
        logger.debug("+++ ClientImpl : Client " + str(client))
        logger.debug("+++ ClientImpl : END print_client")
        return client
