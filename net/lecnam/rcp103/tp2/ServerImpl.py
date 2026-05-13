# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/ServerImpl.py
#
# #####################################################################

import datetime
import os
import platform
import string
import sys
import secrets
import traceback

import logging
import logging.config

from time import time, sleep

import numpy as np

from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.EventType import EventType
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.SimulateurException import SimulateurException

try:
    cfg = ConfigImpl()
    log_path = cfg.get_log_cfg_file_path()

    # Always load logging_config.py from the same directory as this file
    config_path = os.path.join(os.path.dirname(__file__), log_path)
    logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)

    logger = logging.getLogger(__name__)
    # https://docs.python.org/3/library/logging.html#logging-levels

except Exception as e:
    # Fallback to basic logging if config file fails
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to load logging config from {config_path}: {e}")

# Class d'Implémentation
class ServerImpl(IServer):

    mu: int # service rate (mu) of the M/M/1 queue
    server_id: int

    queue: IQueue
    
    def __init__(self, mu: int, server_id: int, queue: IQueue):
        logger.debug(f"+++ ServerImpl : START Constructor")

        self.mu = mu
        self.server_id = server_id
        self.queue = queue

        logger.debug(f"+++ ServerImpl : END Constructor")
    
    def get_queue(self) -> IQueue:
        return self.queue

    def set_queue(self, queue: IQueue):
        self.queue = queue

    def get_server_id(self):
        return self.server_id

    def set_server_id(self, server_id: int):
        self.server_id = server_id

    def listen(self):
        logger.debug(f"+++ ServerImpl : START listen")

        # Loop on Queue messages to dequeue and process them
        while True:
            if not self.queue.is_empty():
                msg = self.queue.dequeue()
                logger.info(f"+++ ServerImpl : Message dequeued : {msg.print_message()}")
                # Process the message (e.g., simulate service time, send response, etc.)
                # For simplicity, we just print the message here
            else:
                #logger.debug(f"+++ ServerImpl : Queue is empty, waiting for messages...")
                # Optionally, add a sleep here to avoid busy waiting
                sleep(0.1)

        logger.debug(f"+++ ServerImpl : END listen")

        def get_server_id():
            return self.server_id
    
        def set_server_id(self, server_id: int):
            self.server_id = server_id

    # --- Affichage ---
    def print_server(self):
        logger.debug(f"+++ ServerImpl : START listen")
        # q = self.queue.print_messages()
        srv = f"[SERVER] ID={self.server_id} | Mu={self.mu}"  
        logger.debug(f"+++ ServerImpl : END listen")        
        return(srv)