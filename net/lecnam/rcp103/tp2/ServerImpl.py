# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/ServerImpl.py
#
#####################################################################

import logging
import logging.config
import os
from time import sleep

import numpy as np

from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.EventType import EventType
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
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
    """
    Serveur avec sa propre queue privée.
    La gateway dispatch les messages dans cette queue (server_id >= 1).
    """

    mu: int        # taux de service (mu)
    server_id: int # identifiant du serveur (>= 1)
    queue: IQueue  # queue privée du serveur
    service_rate: int

    def __init__(self, mu: int, server_id: int, queue: IQueue):
        logger.debug("+++ ServerImpl : START Constructor")
        self.mu = mu
        self.server_id = server_id
        self.queue = queue
        logger.debug(f"+++ ServerImpl : server_id={server_id}, mu={mu}")
        logger.debug("+++ ServerImpl : END Constructor")

    def get_queue(self) -> IQueue:
        return self.queue

    def set_queue(self, queue: IQueue):
        self.queue = queue

    def get_server_id(self):
        return self.server_id

    def set_server_id(self, server_id: int):
        self.server_id = server_id

    def get_mu(self):
        return self.mu

    def listen(self):
        logger.debug(f"+++ ServerImpl : START listen")
        """
        Boucle de traitement : défile et traite les messages
        reçus depuis la gateway.
        """
        logger.debug(f"+++ ServerImpl Server [{self.server_id}] LISTENS ...")
        while True:
            try:
                if not self.queue._lock.acquire(timeout=0.1):
                    logger.warning("+++ ServerImpl : Lock non disponible, échec de count_messages")
                    return None
                else:       
                    if not self.queue.is_empty():
                        msg = self.queue.dequeue()
                        logger.info(
                            f"+++ ServerImpl [{self.server_id}] : DEPT "
                            f"msg id={msg.get_message_id()} "
                            f"src={msg.get_source()} @ t={msg.get_timestamp():.4f}"
                        )
                        # Simulation du temps de service (optionnel)
                        # service_time = np.random.exponential(1.0 / self.mu)
                        # sleep(service_time)
                    else:
                        sleep(0.01)  # évite le busy-wait
            except Exception as e:
                logger.error(f"+++ ServerImpl : Error occurred while listening ...")
            except RuntimeError as error:
                print("+++ ServerImpl : Erreur au Runtime while listening ...")
                print(f"A {type(error).__name__} has occurred.")
                #exit(42)
            finally:    
                self.queue._lock.release()  # ← ajout
                logger.debug(f"+++ ServerImpl : Lock released in listen()")
                
        logger.debug(f"+++ ServerImpl [{self.server_id}] : END listen")
        logger.debug(f"+++ ServerImpl : END listen")

    # --- Affichage ---
    def print_server(self):
        logger.debug(f"+++ ServerImpl : START print_server")
        # q = self.queue.print_messages()
        srv = f"[SERVER] ID={self.server_id} | Mu={self.mu}"  
        logger.debug(f"+++ ServerImpl : END print_server")        
        return(srv)