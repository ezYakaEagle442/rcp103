#!/usr/bin/python3

# Commande pour lancer le programme : 
# PYTHONPATH=. python3 net/lecnam/rcp103/tp2/QueueImplTest.py
# en Linux/WSL: python3 -m net.lecnam.rcp103.tp2.QueueImplTest
# sous Windows/PowerShell: python QueueImplTest.py

from datetime import datetime
import secrets
import traceback
import logging
import os

from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.tp2.QueueImpl import QueueImpl
# from net.lecnam.rcp103.tp2.Poisson import Poisson
from net.lecnam.rcp103.tp2 import Distribution

import numpy as np


try:
    cfg = ConfigImpl()
    log_path = cfg.get_log_cfg_file_path()

    # Always load logging_config.py from the same directory as this file
    config_path = os.path.join(os.path.dirname(__file__), log_path)
    logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)

    logger = logging.getLogger(__name__)
    # https://docs.python.org/3/library/logging.html#logging-levels

    logger.debug(f"+++ QueueImplTest : START")

    seed = cfg.get_seed()
    rng = np.random.default_rng(seed=seed)

    #fish = Poisson(rng=secrets.SystemRandom(), lam=4)
    impl = QueueImpl(lam=4, mu=8)
    q = impl.print_queue()

    logger.info(f"+++ QueueImplTest : q = {q}")

    logger.debug(f"+++ QueueImplTest : END")

except RuntimeError as error:
    logger.error("Erreur au Runtime dans QueueImplTest")
    print(f"A {type(error).__name__} has occurred.")
    exit(42)
except Exception as exception :
        logger.error(f"Exception dans QueueImplTest/Main")
        print(f"A {type(exception).__name__} has occurred.")
        print("")
        traceback.print_exc()
        print("")
        print(exception)
        exit(42)
