# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/QueueImpl.py
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

from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.SimulateurException import SimulateurException

import queue
import numpy as np

from net.lecnam.rcp103.tp2.IMessage import IMessage

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

logger.debug(f"+++ QueueImpl : Test before class")

# Class d'Implémentation
class QueueImpl(IQueue):
 
    queue_size = -1 # If maxsize is <= 0, the queue size is infinite.
    queue: np.array[IMessage]
    # mu: int # service rate (mu) of the M/M/1 queue
    # lam: int # arrival rate (lambda) of the Poisson distribution
            
    def __init__(self):
        logger.debug(f"+++ QueueImpl : START Constructor")
        self.queue = []
        logger.debug(f"+++ QueueImpl : END Constructor")

    def enqueue(self, msg: IMessage):
        logger.debug(f"+++ QueueImpl : START enqueue")
        self.queue.append(msg)
        logger.debug(f"+++ QueueImpl : END enqueue")    

    def dequeue(self, msg: IMessage):
        logger.debug(f"+++ QueueImpl : START dequeue")
        if len(self.queue) == 0:
            logger.error(f"+++ QueueImpl : dequeue called on an empty queue")
            return None
        else:
            msg = self.queue.pop(0) # [1, 2, 3, 4] -> pop(0) -> 1
            logger.debug(f"+++ QueueImpl : Dequeued message with id={msg.get_message_id()}")
            logger.debug(f"+++ QueueImpl : END dequeue")
            return msg
        
    def count_messages(self):
        logger.debug(f"+++ QueueImpl : START count_messages")
        nb_msg = len(self.queue)
        logger.debug(f"+++ QueueImpl : count_messages = {nb_msg}")
        logger.debug(f"+++ QueueImpl : END count_messages")
        return nb_msg


    """ --- Affichage de TOUS les messages --- """
    def print_messages(self):
        logger.debug(f"+++ QueueImpl : START print_messages")

        for msg in self.queue:
            all_messages += msg.print_message()
            
        logger.info(all_messages)
        logger.debug(f"+++ QueueImpl : END print_messages")
        return all_messages