#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/ConfigImplTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.ConfigImplTest
# sous Windows/PowerShell: python ConfigImplTest.py

from datetime import datetime
import traceback
import logging
import os

from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

try:
    logger.debug(f"+++ ConfigImplTest : START")
    cfg = ConfigImpl()
    out_dir = cfg.get_output_dir()
    seed = cfg.get_seed()
    log_path = cfg.get_log_cfg_file_path()
    conf = cfg.print_config()
    logger.info(f"+++ ConfigImplTest : seed= {seed}")
    logger.info(f"+++ ConfigImplTest : out_dir= {out_dir}")
    logger.info(f"+++ ConfigImplTest : log_cfg_file_path= {log_path}")
    logger.info(f"+++ ConfigImplTest : Config created: {conf}")
    logger.debug(f"+++ ConfigImplTest : END")

except RuntimeError as error:
    logger.error("Erreur au Runtime dans ConfigImplTest")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        logger.error(f"Exception dans ConfigImplTest/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
