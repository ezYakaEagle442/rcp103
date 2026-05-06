
# Interface
from abc import ABC, abstractmethod

from net.lecnam.rcp103 import logging_config

class IConfig(ABC):

    @abstractmethod
    def get_seed() -> int:
        pass
    
    def get_output_dir() -> str:
        pass
    
    def get_log_cfg_file_path() -> str:
        pass
    
    # --- Affichage ---
    def print_config():
        pass