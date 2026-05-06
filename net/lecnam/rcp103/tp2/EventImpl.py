# !/usr/bin/python3

# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/EventImpl.py

# rapport à rédiger: overleaf.com

#####################################################################
#
# pre-req: in VSCode install extension 'Microsoft Python Environments Extension' ('Python Environment Manager' is deprecated)
# https://scipy.org/install/: sudo apt-get install python3-scipy
# test in shell with : pip list

# Install on Windows:
# c:\python314\python.exe -m pip install matplotlib

# https://matplotlib.org/stable/install/index.html
# sudo apt upgrade
# sudo apt install python3-matplotlib
# pip install matplotlib
# python3 -m pip install -U pip
# python3 -m pip install -U matplotlib
#  
# To manually trigger a refresh in VSCode:
# Open the Command Palette (Cmd+Shift+P or Ctrl+Shift+P)
# Run Python Environments: Refresh All Environment Managers
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

from net.lecnam.rcp103.SimulateurException import SimulateurException

from scipy.stats import poisson
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html


import numpy as np


import matplotlib.pyplot as plt

import scipy

from net.lecnam.rcp103.tp2.IEvent import IEvent
from net.lecnam.rcp103.tp2.IMessage import IMessage
from net.lecnam.rcp103.tp2.EventType import EventType

# print(scipy.__version__) 

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

# Class d'Implémentation
class EventImpl(IEvent):

    seed= 3 # correspond au Groupe 3
    OUPUT_DIR = "RCP103_TP2_OUTPUTS"

    eventID: int
    message: IMessage
    eventType: string # EventType – SEND_MSG, RECV_MSG, MSG_DEPT
    eventTime: float # horodatage de l'événement
    
    def __init__(self, eventID: int, message: IMessage, eventType: string, eventTime: float):
        self.eventID = eventID
        self.message = message
        self.eventTime = eventTime

        if eventType not in [e.name for e in EventType]:
            logger.error(f"+++ EventImpl __init__  Invalid event type in Constructor: {eventType}. Must be one of: {[e.name for e in EventType]}")
            raise ValueError(f"Invalid event type. Must be one of: {[e.name for e in EventType]}")
        self.eventType = eventType

    def get_event_time(self) ->  datetime.datetime:
        return self.eventTime

    def get_event_type(self) ->  string:
        return self.eventType

    def set_event_time(self, time: datetime):
        self.eventTime = time

    def set_event_type(self, type: string):

        try:
            logger.debug("+++ EventImpl : START setEventType ...")
            if type not in [e.name for e in EventType]:
                logger.error(f"Invalid event type: {type}. Must be one of: {[e.name for e in EventType]}")
                raise ValueError(f"Invalid event type. Must be one of: {[e.name for e in EventType]}")
            self.eventType = type
            logger.debug("+++ EventImpl : evtType = " + str(type))
            logger.debug("+++ EventImpl : END setEventType ...")
        except KeyError:
            raise ValueError(f"Invalid event type: {type}. Must be one of: {[e.name for e in EventType]}")

    def get_message(self) -> IMessage:
        return self.message
    
    def set_message(self, message: IMessage):
        self.message = message
        
    def print_event(self):
        msg = self.get_message().print_message()
        logger.debug(f"+++ EventImpl : START print_event msg={msg}")
        return(f"Event ID: {self.eventID}, Type: {self.eventType}, Time: {self.eventTime}, Message: {msg}\n")