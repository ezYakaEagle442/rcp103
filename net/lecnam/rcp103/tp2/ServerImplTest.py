#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/ServerImplTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.ServerImplTest
# sous Windows/PowerShell: python ServerImplTest.py

from datetime import datetime

import traceback
import logging
import os

from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.tp2.ServerImpl import ServerImpl

from net.lecnam.rcp103.tp2.MessageImpl import MessageImpl
from net.lecnam.rcp103.tp2.IServer import IServer
from net.lecnam.rcp103.tp2.IQueue import IQueue
from net.lecnam.rcp103.tp2.ServerImpl import ServerImpl
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
from net.lecnam.rcp103.tp2.Poisson import Poisson
from net.lecnam.rcp103.tp2.Poisson import Distribution

try:
    cfg = ConfigImpl()
    log_path = cfg.get_log_cfg_file_path()

    # Always load logging_config.py from the same directory as this file
    config_path = os.path.join(os.path.dirname(__file__), log_path)
    logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)

    logger = logging.getLogger(__name__)
    # https://docs.python.org/3/library/logging.html#logging-levels

    logger.debug(f"+++ ServerImplTest : START")
    queue = QueueImpl()
    impl = ServerImpl(8, 1, queue)

    pretty_srv = impl.print_server()
    logger.debug("+++ ServerImplTest : Server created:" + str(pretty_srv))

    impl.listen()

    logger.debug(f"+++ ServerImplTest : END")

except RuntimeError as error:
    logger.error(f"Erreur au Runtime dans ServerImplTest")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        logger.error(f"Exception dans ServerImplTest/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
