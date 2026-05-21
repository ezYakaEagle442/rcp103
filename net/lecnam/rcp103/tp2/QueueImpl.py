# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/QueueImpl.py
#
######################################################################


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
import threading  # ← ajout

import logging
import logging.config

from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.SimulateurException import SimulateurException
from net.lecnam.rcp103.tp2.IMessage import IMessage

import queue
import numpy as np

from collections import deque # pour implémenter une queue thread-safe avec FIFO

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

# Class d'Implémentation
class QueueImpl(IQueue):
 
    queue_size = -1 # If maxsize is <= 0, the queue size is infinite.
    queue: deque[IMessage]
    # mu: int # service rate (mu) of the M/M/1 queue
    # lam: int # arrival rate (lambda) of the Poisson distribution
    dropped_messages: int

    def __init__(self,  max_size:int):
        logger.debug(f"+++ QueueImpl : START Constructor")
        logger.debug(f"+++ QueueImpl : max_queue_size={max_size}")
        self.queue = deque() # Use deque for efficient FIFO
        self._lock = threading.Lock()  # ← ajout
        self.queue_size = max_size  # -1 = infini
        self.dropped_messages = 0
        logger.debug(f"+++ QueueImpl : END Constructor")

    def enqueue(self, msg: IMessage):
        logger.debug("+++ QueueImpl : START enqueue")
        logger.debug(f"+++ QueueImpl : max_queue_size={self.queue_size}")
    
        nb_msg = len(self.queue)
        logger.debug(f"+++ QueueImpl : current_queue_size={nb_msg}")

        with self._lock:
            if self.queue_size > 0 and nb_msg >= self.queue_size:
                self.dropped_messages += 1
                logger.warning(f"+++ QueueImpl : msg {msg.get_message_id()} DROPPED (queue pleine, taille={self.queue_size})")
                return False  # message droppé
            self.queue.append(msg)
        logger.debug("+++ QueueImpl : END enqueue")
        return True     

    def dequeue(self):
        logger.debug(f"+++ QueueImpl : START dequeue")
        with self._lock:  # ← ajout
            if len(self.queue) == 0:
                logger.error(f"+++ QueueImpl : dequeue called on an empty queue")
                return None
            msg = self.queue.popleft()  # FIFO
            logger.info(f"+++ QueueImpl : Dequeued message with id={msg.get_message_id()}")
        logger.debug(f"+++ QueueImpl : END dequeue")
        return msg
    
    def get_dropped_messages(self):
        return self.dropped_messages

    def get_queue_size(self) -> int:
        return len(self.queue)

    def count_messages(self):
        logger.debug(f"+++ QueueImpl : START count_messages")
        with self._lock:  # ← ajout
            nb_msg = len(self.queue)
        logger.debug(f"+++ QueueImpl : count_messages = {nb_msg}")
        logger.debug(f"+++ QueueImpl : END count_messages")
        return nb_msg

    def is_empty(self):
        with self._lock:  # ← ajout
            return len(self.queue) == 0

    """ --- Affichage de TOUS les messages --- """
    def print_messages(self):
        logger.debug(f"+++ QueueImpl : START print_messages")
        with self._lock:  # ← ajout
            if len(self.queue) == 0:
                logger.info(f"+++ QueueImpl : No messages in the queue to print.")
                return None
            all_messages = ""
            for msg in self.queue:
                all_messages += msg.print_message()
        logger.info(all_messages)
        logger.debug(f"+++ QueueImpl : END print_messages")
        return all_messages