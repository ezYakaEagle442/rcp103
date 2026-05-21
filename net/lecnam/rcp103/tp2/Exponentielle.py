#!/usr/bin/python3

# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/tp2/Exponentielle.py

import os
import traceback
import logging
import logging.config

import numpy as np

from net.lecnam.rcp103.tp2.ConfigImpl import ConfigImpl
from net.lecnam.rcp103.tp2.Distribution import Distribution

cfg = ConfigImpl()
log_path = cfg.get_log_cfg_file_path()
config_path = os.path.join(os.path.dirname(__file__), log_path)
logging.config.fileConfig(config_path, defaults=None, disable_existing_loggers=False, encoding=None)
logger = logging.getLogger(__name__)

class Exponentielle(Distribution):
    """Distribution de Exponentielle."""

    seed = cfg.get_seed()
    rng = np.random.default_rng(seed=seed)

    def __init__(self, rng, lam: float):
        logger.debug(f"+++ Exponentielle __init__ : START")
        logger.info(f"+++ Exponentielle __init__ seed={self.seed}, lam={lam}")
        super().__init__(f"Exponentielle (λ={lam})", rng)
        self.lam = lam
        logger.debug(f"+++ Exponentielle __init__ : END")

    def generate(self, n: int) -> np.ndarray:
        return self.rng.exponential(1 / self.lam, size=n)