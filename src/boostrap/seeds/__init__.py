from collections.abc import Callable
from typing import Sequence

from src.boostrap.seeds.bottle_seed import seed_bottles

SeedFunc = Callable[[], None]
REGISTERY: Sequence[SeedFunc] = [
    seed_bottles,
]


def run_seeds() -> None:
    for seed in REGISTERY:
        seed()

