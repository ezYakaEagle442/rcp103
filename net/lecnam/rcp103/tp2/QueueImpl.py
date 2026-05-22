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
        logger.debug(f"+++ QueueImpl : check if Constructor got a lock {self._lock.locked()}") # locked() Returns True if the lock is currently acquired by any thread (no owner info for Lock).
        logger.debug(f"+++ QueueImpl : END Constructor")

    def enqueue(self, msg: IMessage):
        logger.debug("+++ QueueImpl : START enqueue")
        logger.debug(f"+++ QueueImpl : max_queue_size={self.queue_size}")
        nb_msg = 0
        try:
            nb_msg = self.count_messages()
            logger.debug(f"+++ QueueImpl : current_queue_size={nb_msg}")

            if not self._lock.acquire(timeout=0.1):
                logger.warning("+++ QueueImpl : Lock non disponible, échec de enqueue")
                return None
            else:
                if self.queue_size > 0 and nb_msg >= self.queue_size:
                    self.dropped_messages += 1
                    logger.warning(f"+++ QueueImpl : msg {msg.get_message_id()} DROPPED (queue pleine, taille={self.queue_size})")
                    return False  # message droppé
                self.queue.append(msg)
        except Exception as e:
            logger.error(f"+++ QueueImpl : Error occurred while enqueuing message: {e}")
        finally:
            self._lock.release()  # ← ajout
            logger.debug("+++ QueueImpl : Lock released in enqueue()")

        logger.debug("+++ QueueImpl : END enqueue")
        return True     

    def dequeue(self):
        logger.debug(f"+++ QueueImpl : START dequeue")
        try:
            if not self._lock.acquire(timeout=0.1):
                logger.warning("+++ QueueImpl : Lock non disponible, échec de dequeue")
                return None
            else:
                if self.is_empty():
                    logger.error(f"+++ QueueImpl : dequeue called on an empty queue")
                    return None

                nb_msg =self.count_messages()
                logger.debug(f"+++ QueueImpl : dequeue current_queue_size={nb_msg}")

                msg = self.queue.popleft()  # FIFO
                logger.info(f"+++ QueueImpl : Dequeued message with id={msg.get_message_id()}")
                nb_msg = self.count_messages()
                logger.info(f"+++ QueueImpl : current_queue_size={nb_msg}")

        except Exception as e:
            logger.error(f"+++ QueueImpl : Error occurred while dequeuing message: {e}")
        finally:
            self._lock.release()  # ← ajout
            logger.debug("+++ QueueImpl : Lock released in dequeue()")

        logger.debug(f"+++ QueueImpl : END dequeue")
        return msg
    
    def get_dropped_messages(self):
        logger.debug(f"+++ QueueImpl : START get_dropped_messages")
        logger.debug(f"+++ QueueImpl : END get_dropped_messages")
        return self.dropped_messages

    def get_queue_size(self) -> int:
        logger.debug(f"+++ QueueImpl : START get_queue_size")
        logger.debug(f"+++ QueueImpl : END get_queue_size")        
        return len(self.queue)

    def count_messages(self):
        logger.debug(f"+++ QueueImpl : START count_messages")
        nb_msg = 0
        try:
            if not self._lock.acquire(timeout=0.1):
                logger.warning("+++ QueueImpl : Lock non disponible, échec de count_messages")
                return None
            else:
                logger.debug(f"+++ QueueImpl : count_messages get a lock {self._lock.locked()}") # locked() Returns True if the lock is currently acquired by any thread (no owner info for Lock).
                with self._lock:  # ← ajout
                    nb_msg = len(self.queue)
                logger.debug(f"+++ QueueImpl : count_messages = {nb_msg}")
        except Exception as e:
            logger.error(f"+++ QueueImpl : Error occurred while counting messages: {e}")
        except RuntimeError as error:
            logger.error("+++ QueueImpl : Erreur au Runtime dans count_messages()")
            logger.error(f"A {type(error).__name__} has occurred.")
            exit(42)
        finally:    
            self._lock.release()  # ← ajout
            logger.debug(f"+++ QueueImpl : Lock released in count_messages()")

        logger.debug(f"+++ QueueImpl : END count_messages")
        return nb_msg

    def is_empty(self):
        logger.debug(f"+++ QueueImpl : START is_empty")
        try:
            with self._lock:  # ← ajout
                return len(self.queue) == 0
        except Exception as e:
            logger.error(f"+++ QueueImpl : Error occurred while checking if queue is empty: {e}")
            return False
        finally:
            self._lock.release()  # ← ajout
            logger.debug(f"+++ QueueImpl : Lock released in is_empty()")
            logger.debug(f"+++ QueueImpl : END is_empty")

    """ --- Affichage de TOUS les messages --- """
    def print_messages(self):
        logger.debug(f"+++ QueueImpl : START print_messages")
        try:
            with self._lock:  # ← ajout
                if self.is_empty():
                    logger.info(f"+++ QueueImpl : No messages in the queue to print.")
                    return None
                all_messages = ""
                for msg in self.queue:
                    all_messages += msg.print_message()
            logger.info(all_messages)
        except Exception as e:
            logger.error(f"+++ QueueImpl : Error occurred while printing messages: {e}")
        finally:
            self._lock.release()  # ← ajout
            logger.debug(f"+++ QueueImpl : Lock released in print_messages()")

        logger.debug(f"+++ QueueImpl : END print_messages")
        return all_messages