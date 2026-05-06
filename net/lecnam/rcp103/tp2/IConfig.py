
# Interface
from abc import ABC, abstractmethod

class IConfig(ABC):

    @abstractmethod
    def get_seed() -> int:
        pass
    
    def get_output_dir() -> str:
        pass
    
    # --- Affichage ---
    def print_config():
        pass