# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/ClientImpl.py
#
# #####################################################################

from abc import abstractmethod
import datetime
import os
import platform
import string
import sys
import secrets
import traceback

import logging
import logging.config

from scipy.stats import poisson
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html

import numpy as np
import matplotlib.pyplot as plt
import scipy

from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.EventType import EventType
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.SimulateurException import SimulateurException
from net.lecnam.rcp103.tp2 import IQueue
from net.lecnam.rcp103.tp2.Poisson import Poisson
from net.lecnam.rcp103.tp2.Poisson import Distribution
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
from net.lecnam.rcp103.tp2.IServer import IServer

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

# Class d'Implémentation
class ClientImpl(IClient):

    message: IMessage
    arrival_rate: int # arrival rate (lambda) of the Poisson distribution
    queue: IQueue
    client_id: int
    destination: IServer

    def __init__(self, arrival_rate: int):
        logger.debug(f"+++ ClientImpl : START Constructor")

        seed = cfg.get_seed()
        rng = np.random.default_rng(seed=seed)

        fish = Poisson(rng=rng, lam=self.arrival_rate)
        impl = QueueImpl(lam=fish)
        
        logger.debug(f"+++ ClientImpl : END Constructor")

    def send_message(self, msg: IMessage):
        logger.debug(f"+++ ClientImpl : START send_message")
        self.queue.enqueue(msg)
        logger.debug(f"+++ ClientImpl : END send_message")

    def set_client_id(self, id: int):
        self.client_id = id

    @abstractmethod
    def get_client_id(self):
        return self.client_id
    
    def get_destination(self):
        return self.destination

    # Set Queue name
    def set_destination(self, dst: IServer):
        self.destination = dst

    def get_arrival_rate(self):
        return self.arrival_rate

    def set_arrival_rate(self, rate: int):
        self.arrival_rate = rate

    @abstractmethod
    def set_message(self, msg: IMessage):
        self.message = msg

    @abstractmethod
    def get_message(self, msg: IMessage):
        return self.message

    # --- Affichage ---
    def print_client(self):
        logger.debug(f"+++ ClientImpl : START print_client")
        
        logger.debug(f"+++ ClientImpl : END print_client")        
        return(f"TODO")
