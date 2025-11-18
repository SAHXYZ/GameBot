# filename: utils/coins.py

"""
Coin conversion utilities.

Denominations:
1 Bronze = 1 bronze unit
1 Silver = 100 bronze
1 Gold = 100 Silver = 10_000 bronze
1 Platinum = 1000 Gold = 10_000_000 bronze
Black Gold = special (non-convertible here; treated as a separate value)
"""

BRONZE_PER_SILVER = 100
BRONZE_PER_GOLD = BRONZE_PER_SILVER * 100      # 100 * 100 = 10_000
BRONZE_PER_PLATINUM = BRONZE_PER_GOLD * 1000    # 10_000 * 1000 = 10_000_000

def breakdown_from_bronze(total_bronze: int):
    """
    Convert total bronze units into (platinum, gold, silver, bronze).
    Black gold must be handled separately.
    Returns dict with keys: platinum, gold, silver, bronze
    """
    if total_bronze < 0:
        total_bronze = 0

    platinum = total_bronze // BRONZE_PER_PLATINUM
    rem = total_bronze % BRONZE_PER_PLATINUM

    gold = rem // BRONZE_PER_GOLD
    rem = rem % BRONZE_PER_GOLD

    silver = rem // BRONZE_PER_SILVER
    bronze = rem % BRONZE_PER_SILVER

    return {
        "platinum": int(platinum),
        "gold": int(gold),
        "silver": int(silver),
        "bronze": int(bronze)
    }

def total_bronze_value(user_coins: dict):
    """
    Compute total bronze-equivalent value for ranking.
    Includes platinum, gold, silver, bronze. Black_gold is treated externally.
    """
    plat = int(user_coins.get("platinum", 0) or 0)
    gold = int(user_coins.get("gold", 0) or 0)
    silver = int(user_coins.get("silver", 0) or 0)
    bronze = int(user_coins.get("bronze", 0) or 0)

    total = (plat * BRONZE_PER_PLATINUM) + (gold * BRONZE_PER_GOLD) + (silver * BRONZE_PER_SILVER) + bronze
    return int(total)
