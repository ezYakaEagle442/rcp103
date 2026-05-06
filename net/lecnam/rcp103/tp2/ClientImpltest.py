#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/ClientImplTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.ClientImplTest
# sous Windows/PowerShell: python ClientImplTest.py

from datetime import datetime
import traceback
import logging
import os

from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.tp2.ClientImpl import ClientImpl

try:
    cfg = ConfigImpl()
    log_path = cfg.get_log_cfg_file_path()

    # Always load logging_config.py from the same directory as this file
    config_path = os.path.join(os.path.dirname(__file__), log_path)
    logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

    logger = logging.getLogger(__name__)
    # https://docs.python.org/3/library/logging.html#logging-levels

    logger.debug(f"+++ ClientImplTest : START")
    impl = ClientImpl()
    xxx = impl.getXXXX()

    logger.info(f"+++ ClientImplTest : xxx = {xxx}")

    logger.debug(f"+++ ClientImplTest : END")

except RuntimeError as error:
    logger.error("Erreur au Runtime dans ClientImplTest")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        logger.error(f"Exception dans ClientImplTest/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
