#!/usr/bin/python3

# PYTHONPATH=. /usr/bin/python3 net/lecnam/rcp103/demo.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Seed = numéro de groupe
rng = np.random.default_rng(seed=3)

ns = [10, 100, 1000, 10000]

distributions = {
    "Uniforme entière (20–40)":
        lambda n: rng.integers(20, 41, size=n),
    "Uniforme réelle (2.0–3.0)":
        lambda n: rng.uniform(2.0, 3.0, size=n),
    "Normale (µ=0, σ=0.5)":
        lambda n: rng.normal(0, 0.5, size=n),
    "Exponentielle (moy=4)":
        lambda n: rng.exponential(scale=4, size=n),
    "Poisson (λ=42)":
        lambda n: rng.poisson(lam=42, size=n),
}

for dist_name, generator in distributions.items():
    fig, axes = plt.subplots(1, 4, figsize=(16, 3))
    fig.suptitle(dist_name, fontsize=13)

    for ax, n in zip(axes, ns):
        data = generator(n)
        ax.hist(data, bins='auto', edgecolor='white', linewidth=0.4)
        ax.set_title(f"n = {n}")
        ax.set_xlabel("Valeur")
        ax.set_ylabel("Fréquence")

    plt.tight_layout()
    plt.savefig(f"hist_{dist_name[:10].strip()}.png", dpi=150)
    plt.show()
