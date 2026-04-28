#!/usr/bin/python3

# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp1/SimulateurCongruantielle.py

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

import os
import platform
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
print(scipy.__version__) 

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

# Class d'Implémentation
class SimulateurCongruantielle():

    seed= 3 # correspond au Groupe 3
    OUPUT_DIR = "RCP103_TP1_OUTPUTS"

    def get_x0(self) -> int:
        return self.x0

    def set_x0(self, value: int) -> None:
        self.x0 = value

    def get_seed(self) -> int:
        return self.seed

    def set_seed(self, value: int) -> None:
        self.seed = value

    # Use Case 1 : distribution uniforme discrète
    def calculUniformDiscrete(self):
        try:
            logger.debug("+++ SimulateurCongruantielle : calculUniformDiscrete en cours...")
            systeme = platform.system()
            print("Système d'exploitation:" + systeme)
            os.makedirs(self.OUPUT_DIR, exist_ok=True)

            rng = np.random.default_rng (seed = self.seed)

            # TOLDO.next
            # Uniforme entière (20–40)": lambda n: rng.integers(20, 41, size=n)
            # Afficher a l’ecran n valeurs differentes pour : n = 10, n = 100, n = 1 000, n = 10 000

            res = []
            # res = rng.integers(20, 41, size=n)

            # print("+++ res = " + str(res))
            logger.debug("+++ SimulateurCongruantielle : calculUniformDiscrete terminé.")

            if res.__len__() == 0:
                raise SimulateurException("Le résultat du calculUniformDiscrete est nul")
            else:
                return res
        
        except RuntimeError as error:
            logger.error("Erreur au Runtime dans SimulateurCongruantielle calculUniformDiscrete")
            logger.error(f"A {type(error).__name__} has occurred.")
            # exit(42)
        except Exception as exception :
                logger.error("Exception dans SimulateurCongruantielle calculUniformDiscrete")
                logger.error(f"A {type(exception).__name__} has occurred.")
                logger.error("")
                traceback.print_exc()
                logger.error("")
                logger.error(exception)
                # exit(42)
                raise 

    # Use Case 2 : distribution uniforme continue
    def calculUniformContinue(self):
        try:
            logger.debug("+++ SimulateurCongruantielle : calculUniformContinue en cours...")
            systeme = platform.system()
            print("Système d'exploitation:" + systeme)
            os.makedirs(self.OUPUT_DIR, exist_ok=True)

            rng = np.random.default_rng (seed = self.seed)
            res = rng.uniform(2.0, 3.0, size=5)
            
        except RuntimeError as error:
            logger.error("Erreur au Runtime dans SimulateurCongruantielle calculUniformContinue")
            logger.error(f"A {type(error).__name__} has occurred.")
            # exit(42)
        except Exception as exception :
                logger.error("Exception dans SimulateurCongruantielle calculUniformContinue")
                logger.error(f"A {type(exception).__name__} has occurred.")
                logger.error("")
                traceback.print_exc()
                logger.error("")
                logger.error(exception)
                # exit(42)
                raise

    # Use Case 3 : distribution normale    
    def calculNormal(self):
        try:
            logger.debug("+++ SimulateurCongruantielle : calculNormal en cours...")
            systeme = platform.system()
            print("Système d'exploitation:" + systeme)
            os.makedirs(self.OUPUT_DIR, exist_ok=True)

            rng = np.random.default_rng (seed = self.seed)
            res = rng.normal(0, 0.5, size=n)


        except RuntimeError as error:
            logger.error("Erreur au Runtime dans SimulateurCongruantielle calculNormal")
            logger.error(f"A {type(error).__name__} has occurred.")
            # exit(42)
        except Exception as exception :
                logger.error("Exception dans SimulateurCongruantielle calculNormal")
                logger.error(f"A {type(exception).__name__} has occurred.")
                logger.error("")
                traceback.print_exc()
                logger.error("")
                logger.error(exception)
                # exit(42)
                raise
        

    # Use Case 4 :    
    def calculExp(self):
        try:
            logger.debug("+++ SimulateurCongruantielle : calculExp en cours...")
            systeme = platform.system()
            print("Système d'exploitation:" + systeme)
            os.makedirs(self.OUPUT_DIR, exist_ok=True)

            rng = np.random.default_rng (seed = self.seed)

            res = rng.exponential(scale=4, size=n)

        except RuntimeError as error:
            logger.error("Erreur au Runtime dans SimulateurCongruantielle calculExp")
            logger.error(f"A {type(error).__name__} has occurred.")
            # exit(42)
        except Exception as exception :
                logger.error("Exception dans SimulateurCongruantielle calculExp")
                logger.error(f"A {type(exception).__name__} has occurred.")
                logger.error("")
                traceback.print_exc()
                logger.error("")
                logger.error(exception)
                # exit(42)
                raise

# Use Case 5 :    
    def calculPoisson(self):
        try:
            logger.debug("+++ SimulateurCongruantielle : calculPoisson en cours...")
            systeme = platform.system()
            print("Système d'exploitation:" + systeme)
            os.makedirs(self.OUPUT_DIR, exist_ok=True)

            rng = np.random.default_rng (seed = self.seed)
            res = rng.poisson(lam = 42, size =5)

        except RuntimeError as error:
            logger.error("Erreur au Runtime dans SimulateurCongruantielle calculPoisson")
            logger.error(f"A {type(error).__name__} has occurred.")
            # exit(42)
        except Exception as exception :
                logger.error("Exception dans SimulateurCongruantielle calculPoisson")
                logger.error(f"A {type(exception).__name__} has occurred.")
                logger.error("")
                traceback.print_exc()
                logger.error("")
                logger.error(exception)
                # exit(42)
                raise
        
    # Fonction d'affichage des figures            
    def displayFigures(distribution, distributionName):
        try:
            logger.debug("+++ SimulateurCongruantielle : START displayFigures ...")


            plt.figure(figsize=(12, 6))
            
            plt.subplot(1, 2, 1)
            plt.plot(x1, marker='o')
            plt.title("Courbe 1")
            plt.xlabel("n")
            plt.ylabel("x_n")
            
            plt.subplot(1, 2, 2)
            plt.plot(x2, marker='o')
            plt.title("Courbe 2")
            plt.xlabel("n")
            plt.ylabel("x_n")
            
            plt.tight_layout()
            plt.show()
         
        except RuntimeError as error:
            logger.error("Erreur au Runtime dans SimulateurCongruantielle displayFigures")
            logger.error(f"A {type(error).__name__} has occurred.")
            # exit(42)
        except Exception as exception :
                logger.error("Exception dans SimulateurCongruantielle displayFigures")
                logger.error(f"A {type(exception).__name__} has occurred.")
                logger.error("")
                traceback.print_exc()
                logger.error("")
                logger.error(exception)
                # exit(42)
                raise 