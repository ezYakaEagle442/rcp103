# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/GatewayImpl.py
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
from rcp103.net.lecnam.rcp103.tp2 import IGateway
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

    queue: IQueue
    server: IServer

    def get_queue(self) ->  IQueue:
        return self.queue

    def set_queue(self, queue: IQueue):
        self.queue = queue
    
    def get_server(self) ->  IServer:
        return self.server

    def set_server(self, server: IServer):
        self.server = server

    def __init__(self, queue: IQueue, server: IServer):
        logger.debug(f"+++ GatewayImpl : START Constructor")
        self.queue = queue
        self.server = server
        logger.debug(f"+++ GatewayImpl : END Constructor")

    # --- Affichage ---
    def print_gateway(self):
        logger.debug(f"+++ GatewayImpl : START print_gateway")
        all_msg = self.get_queue().print_messages()
        logger.debug(f"+++ GatewayImpl : Queue messages = {all_msg}")
        srv = self.server.print_server()
        logger.debug(f"+++ GatewayImpl : SERVER = {srv}")
        logger.debug(f"+++ GatewayImpl : END print_gateway")
        return(f"Server: {srv}, ALL Messages: {all_msg}\n")
