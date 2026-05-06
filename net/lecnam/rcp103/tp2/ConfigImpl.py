# !/usr/bin/python3

#####################################################################
#
# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/ConfigImpl.py
#
# #####################################################################

import os
import logging
import logging.config

from net.lecnam.rcp103.SimulateurException import SimulateurException
from net.lecnam.rcp103.tp2.IConfig import IConfig

# Always load logging_config.py from the same directory as this file
config_path = os.path.join(os.path.dirname(__file__), "logging_config.cnf")
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=True, encoding=None)

logger = logging.getLogger(__name__)
# https://docs.python.org/3/library/logging.html#logging-levels

# Class d'Implémentation
class ConfigImpl(IConfig):

    seed= 3 # correspond au Groupe 3
    OUPUT_DIR = "RCP103_TP2_OUTPUTS"
    
    def __init__(self):
        logger.debug(f"+++ ConfigImpl : START Constructor")
        logger.debug(f"+++ ConfigImpl : END Constructor")
        pass

    def get_seed(self) -> int:
        return self.seed
    
    def get_output_dir(self) -> str:
        return self.OUPUT_DIR
    
    # --- Affichage ---
    def print_config(self):
        return(f"[Config] seed={self.seed} | output_dir={self.OUPUT_DIR}")