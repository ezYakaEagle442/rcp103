#!/usr/bin/python3

# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/demo4.py

import numpy as np
import matplotlib.pyplot as plt

# Classe parente pour les différentes distributions
class Distribution:
    """Classe de base représentant une distribution statistique."""

    def __init__(self, name: str, rng: np.random.Generator):
        self.name = name
        self.rng = rng

    def generate(self, n: int) -> np.ndarray:
        raise NotImplementedError("La méthode generate() doit être implémentée dans la sous-classe.")

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"


class UniformeEntiere(Distribution):
    """Distribution uniforme discrète sur [MIN, MAX]."""

    def __init__(self, rng, low: int = 20, high: int = 41):
        super().__init__(f"Uniforme entière ({low}–{high})", rng)
        self.low = low
        self.high = high

    def generate(self, n: int) -> np.ndarray:
        return self.rng.integers(self.low, self.high + 1, size=n)


class UniformeReelle(Distribution):
    """Distribution uniforme continue sur [MIN, MAX)."""

    def __init__(self, rng, low: float = 2.0, high: float = 3.0):
        super().__init__(f"Uniforme réelle ({low}–{high})", rng)
        self.low = low
        self.high = high

    def generate(self, n: int) -> np.ndarray:
        return self.rng.uniform(self.low, self.high, size=n)


class Normale(Distribution):
    """Distribution normale (gaussienne)."""

    def __init__(self, rng, mu: float = 0, sigma: float = 0.5):
        super().__init__(f"Normale (µ={mu}, σ={sigma})", rng)
        self.mu = mu
        self.sigma = sigma

    def generate(self, n: int) -> np.ndarray:
        return self.rng.normal(self.mu, self.sigma, size=n)


class Exponentielle(Distribution):
    """Distribution exponentielle."""

    def __init__(self, rng, scale: float = 4):
        super().__init__(f"Exponentielle (moy={scale})", rng)
        self.scale = scale

    def generate(self, n: int) -> np.ndarray:
        return self.rng.exponential(self.scale, size=n)


class Poisson(Distribution):
    """Distribution de Poisson."""

    def __init__(self, rng, lam: float = 42):
        super().__init__(f"Poisson (λ={lam})", rng)
        self.lam = lam

    def generate(self, n: int) -> np.ndarray:
        return self.rng.poisson(self.lam, size=n)


class HistogrammeVisualiser:
    """Génère et sauvegarde les histogrammes pour une liste de distributions."""

    def __init__(self, distributions: list[Distribution], ns: list[int]):
        self.distributions = distributions
        self.ns = ns

    def tracer(self, save: bool = True, show: bool = True):
        for dist in self.distributions:
            fig, axes = plt.subplots(1, len(self.ns), figsize=(16, 3))
            fig.suptitle(dist.name, fontsize=13)

            for ax, n in zip(axes, self.ns):
                data = dist.generate(n)
                ax.hist(data, bins='auto', edgecolor='white', linewidth=0.4)
                ax.set_title(f"n = {n}")
                ax.set_xlabel("Valeur")
                ax.set_ylabel("Fréquence")

            plt.tight_layout()

            if save:
                filename = f"hist_{dist.name[:10].strip().encode('utf-8').hex()}.png"
                plt.savefig(filename, dpi=150)

            if show:
                plt.show()

            plt.close(fig)


if __name__ == "__main__":
    print("+++ START TP1 Main ...")
    rng = np.random.default_rng(seed=3)

    distributions = [
        UniformeEntiere(rng),
        UniformeReelle(rng),
        Normale(rng),
        Exponentielle(rng),
        Poisson(rng),
    ]

    ns = [10, 100, 1000, 10000]

    visualiseur = HistogrammeVisualiser(distributions, ns)
    visualiseur.tracer(save=True, show=True)

    print("+++ END TP1 Main.")