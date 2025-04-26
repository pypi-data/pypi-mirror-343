from dataclasses import dataclass

from ..configDict import itemType
from ..inventory.item import InventoryItem


@dataclass(frozen=True)
class MagicElement(InventoryItem):
    id: int
    name: str
    type: itemType


Fire = MagicElement(21, "Fire Element", itemType.FIRE)
Blizzard = MagicElement(22, "Blizzard Element", itemType.BLIZZARD)
Thunder = MagicElement(23, "Thunder Element", itemType.THUNDER)
Cure = MagicElement(24, "Cure Element", itemType.CURE)
Magnet = MagicElement(87, "Magnet Element", itemType.MAGNET)
Reflect = MagicElement(88, "Reflect Element", itemType.REFLECT)
