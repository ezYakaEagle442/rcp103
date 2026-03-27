#!/usr/bin/python3

# PYTHONPATH=. python3 net/lecnam/rcp103/SimulateurImpl.py

import os
import platform
import sys
import secrets
import traceback

import logging
import logging.config

from net.lecnam.rcp103.ISimulateur import ISimulateur
from net.lecnam.rcp103.SimulateurException import SimulateurException

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

# Class d'Implémentation
class SimulateurImpl(ISimulateur):

    name: str
    u: int
    v: int

    def get_name(self) -> str:
        return self.name

    def set_name(self, value: str) -> None:
        self.name = value

    def get_u(self) -> int:
        return self.u

    def set_u(self, value: int) -> None:
        self.u = value

    def get_v(self) -> int:
        return self.v

    def set_v(self, value: int) -> None:
        self.v = value

    def __init__(self, name, valU, valV):
        self.name = name
        self.u = valU
        self.v = valV
        
    def calcul(self, x: int, y: int):
        try:
            logger.debug("+++ SimulateurImpl : Calcul en cours...")
            logger.debug(" x = " + str(x) + " y = " + str(y))
            systeme = platform.system()
            print("Système d'exploitation:" + systeme)

            proba = [0.1, 0.2, 0.3, 0.4]
            c=secrets.choice(proba)
            print("+++ proba = " + str(c))

            # créer une instance de SystemRandom
            secure_rand = secrets.SystemRandom()
            nb = secure_rand.random() # secure_rand.randint(a=0, b=1)
            print("+++ nb = " + str(nb))
            res = (x + y) * nb
            print("+++ res = " + str(res))
            logger.debug("+++ SimulateurImpl : Calcul terminé.")

            if res == 0:
                raise SimulateurException("Le résultat du calcul est nul", {"x": x, "y": y, "nb": nb})
            else:
                return res
        
        except RuntimeError as error:
            logger.error("Erreur au Runtime dans SimulateurImpl")
            logger.error(f"A {type(error).__name__} has occurred.")
            # exit(42)
        except Exception as exception :
                logger.error("Exception dans Main")
                logger.error(f"A {type(exception).__name__} has occurred.")
                logger.error("")
                traceback.print_exc()
                logger.error("")
                logger.error(exception)
                # exit(42)
                raise 