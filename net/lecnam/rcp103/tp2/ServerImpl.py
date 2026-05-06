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

from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.EventType import EventType
from net.lecnam.rcp103.tp2.IClient import IClient
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.SimulateurException import SimulateurException

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels
# Class d'Implémentation
class ServerImpl(IServer):

    eventID: int
    message: IMessage
    eventType: string # EventType – SEND_MSG, RECV_MSG, MSG_DEPT
    eventTime: float # horodatage de l'événement
    
    def __init__(self):
        logger.debug(f"+++ ServerImpl : START Constructor")
        logger.debug(f"+++ ServerImpl : END Constructor")
        pass

    # --- Affichage ---
    def print_server(self):
        return(f"TODO")
