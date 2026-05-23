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
    srv_proc: int

    def __init__(self, mu: int, server_id: int, queue: IQueue):
        logger.debug("+++ ServerImpl : START Constructor")
        self.mu = mu
        self.server_id = server_id
        self.queue = queue
        self.srv_proc = 42
        logger.debug(f"+++ ServerImpl : server_id={server_id}, mu={mu}")
        logger.debug("+++ ServerImpl : END Constructor")

    def get_srv_proc(self) -> int:
        return self.srv_proc

    def set_srv_proc(self, srv_proc: int):
        self.srv_proc = srv_proc

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
                srv_id = self.get_server_id()
                srv_proc = self.get_srv_proc()
                locked_down = self.queue._lock.locked() # just to check if lock is acquired
                logger.info(f"+++ ServerImpl listen : srv_id = {srv_id} | Lock bien disponible le Server va pouvoir écouter ! Lock status: {locked_down}")
                logger.info(f"+++ ServerImpl : srv_proc = {srv_proc}")
                file_vide = self.queue.is_empty()
                logger.debug(f"+++ ServerImpl listen : srv_id = {srv_id} | file_vide = {file_vide}")

                if srv_proc == srv_id:
                    logger.info(f"+++ ServerImpl listen : srv_id={srv_id} does match srv_proc={srv_proc}")

                    if not file_vide:
                        logger.info(f"+++ ServerImpl listen : srv_id = {srv_id} | Queue is NOT empty ! Server ID {srv_id} can dequeue a message.")
                        self.get_queue().set_srv_caller_id(srv_id) # set the caller id for logging purposes

                        msg = self.queue.dequeue()
                        if (msg is None):
                            logger.warning(f"+++ ServerImpl : srv_id = {srv_id} | Failed to dequeue a message due to lock acquisition failure. Will retry in the next iteration.")
                            sleep(0.42)  # évite le busy-wait si le message n'est pas destiné à ce serveur
                            continue

                        destination_dispatched_by_gw = msg.get_destination() # check if destination does match wit hcurrent Server ID
                        logger.debug(f"+++ ServerImpl listen : Message dequeued, checking destination ... {destination_dispatched_by_gw} vs Server ID {srv_id}")
                        # self.queue._lock.release() # ← ajout : release du lock après le dequeue, avant de traiter le message
                        if srv_id == destination_dispatched_by_gw:
                            logger.info(
                                f"+++ ServerImpl listen SERVER {self.server_id}] listen has SUCCESSFULLY serverd  "
                                f"msg id={msg.get_message_id()} "
                                f"src-client ID={msg.get_source()} "
                                f"@ t={msg.get_timestamp():.4f}"
                            )
                            # Simulation du temps de service (optionnel)
                            service_time = np.random.exponential(1.0 / self.mu)
                            sleep(service_time)

                        else:
                            logger.warning(f"+++ ServerImpl listen : Message destination {destination_dispatched_by_gw} does not match Server ID {srv_id}, leave it in the queue")
                            # this message should be put back in the queue or handled by the next server, but since we are using a simple queue without peeking, we just let it be and the next server will handle it in the next iteration
                            #enqueued_back = self.queue.enqueue(msg)  # re-enqueue the message if it's not for this server
                            #logger.debug(f"+++ ServerImpl : Enqueue success: {enqueued_back} | Message with id={msg.get_message_id()} re-enqueued back to the queue for the next server to handle it")
                            #if (enqueued_back == False):
                            #    logger.warning(f"+++ ServerImpl listen : Failed to re-enqueue message with id={msg.get_message_id()} back to the queue after dequeueing it because it was not for this server. Message is DROPPED.")
                            sleep(0.01)  # évite le busy-wait si le message n'est pas destiné à ce serveur
                    else:
                        logger.debug(f"+++ ServerImpl listen : else file_vide = {file_vide}")
                        sleep(0.01)  # évite le busy-wait

                    # reset to default value after processing the message for this server
                    self.set_srv_proc(42)

                else:
                    logger.warning(f"+++ ServerImpl : srv_id = {srv_id} | srv_proc = {srv_proc} | Message is not for this server, skipping ...")
                    sleep(0.01)  # évite le busy-wait si le message n'est pas destiné à ce serveur

            except Exception as e:
                logger.error(f"+++ ServerImpl : Error occurred while listening ... {e}")
            except RuntimeError as error:
                print("+++ ServerImpl listen : Erreur au Runtime while listening ...")
                print(f"A {type(error).__name__} has occurred.")
                #exit(42)
            finally:    
                # self.queue._lock.release()  # ← ajout
                #logger.debug(f"+++ ServerImpl : Lock released in listen()")
                logger.debug(f"+++ ServerImpl [{self.server_id}] : END listen")

    # --- Affichage ---
    def print_server(self):
        logger.debug(f"+++ ServerImpl : START print_server")
        # q = self.queue.print_messages()
        srv = f"[SERVER] ID={self.server_id} | Mu={self.mu}"  
        logger.debug(f"+++ ServerImpl : END print_server")        
        return(srv)