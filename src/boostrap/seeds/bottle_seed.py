from __future__ import annotations

from src.features.sea.bottle.bottle_entity import BottleEntity

SEED_COUNT = 15
SEED_SENTINEL = "__seeded_bottle__"


def seed_bottles() -> None:
    seeded = BottleEntity.find(BottleEntity.creator == SEED_SENTINEL).all()
    if seeded:
        return

    for index in range(SEED_COUNT):
        BottleEntity(
            type="text",
            content=f"Sample bottle content #{index}",
            creator=SEED_SENTINEL,
        ).save()

