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

try:
    cfg = ConfigImpl()
    log_path = cfg.get_log_cfg_file_path()

    # Always load logging_config.py from the same directory as this file
    config_path = os.path.join(os.path.dirname(__file__), log_path)
    logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

    logger = logging.getLogger(__name__)
    # https://docs.python.org/3/library/logging.html#logging-levels

    logger.debug(f"+++ ServerImplTest : START")
    impl = ServerImpl()
    xxx = impl.getXXXX()

    logger.info(f"+++ ServerImplTest : xxx = {xxx}")

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
