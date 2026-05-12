#!/usr/bin/python3

# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/Distribution.py

import os
import traceback
import logging
import logging.config

import numpy as np

from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)
seed = cfg.get_seed()
rng = np.random.default_rng(seed=seed)
logger = logging.getLogger(__name__)

# Classe parente pour les différentes distributions
class Distribution:
    """Classe de base représentant une distribution statistique."""

    def __init__(self, name: str, rng):
        logger.debug(f"+++ Distribution __init__ : START")
        self.name = name
        self.rng = rng
        logger.debug(f"+++ Distribution __init__ : END")

    def generate(self, n: int) -> np.ndarray:
        raise NotImplementedError("La méthode generate() doit être implémentée dans la sous-classe.")

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"
