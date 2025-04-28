import datetime
import pytest
from main import Stem, Branch, stem_from_year, branch_from_year, stem_from_day, branch_from_day

def test_stem_from_year():
    assert stem_from_year(2024) == Stem.WOOD_YANG  # 甲
    assert stem_from_year(1984) == Stem.WOOD_YANG  # 甲 (60年前)
    assert stem_from_year(2023) == Stem.WATER_YIN # 癸
    assert stem_from_year(2025) == Stem.WOOD_YIN  # 乙

def test_branch_from_year():
    assert branch_from_year(2024) == Branch.DRAGON # 辰
    assert branch_from_year(1984) == Branch.RAT    # 子 (60年前)
    assert branch_from_year(2023) == Branch.RABBIT # 卯
    assert branch_from_year(2025) == Branch.SNAKE  # 巳

def test_stem_from_day():
    # Base date used in the function
    base_date = datetime.date(2025, 4, 24)
    assert stem_from_day(base_date) == Stem.WATER_YIN # 癸

    # Another known date (Result based on 2025-04-24 base date)
    known_date_1 = datetime.date(2000, 1, 1)
    assert stem_from_day(known_date_1) == Stem.EARTH_YANG # 戊 (Expected Metal Yang with 2000-01-01 base)

    # Date after base date
    known_date_2 = datetime.date(2025, 4, 25)
    assert stem_from_day(known_date_2) == Stem.WOOD_YANG # 甲

    # Date before base date
    known_date_3 = datetime.date(2025, 4, 23)
    assert stem_from_day(known_date_3) == Stem.WATER_YANG # 壬

def test_branch_from_day():
    # Base date used in the function
    base_date = datetime.date(2025, 4, 24)
    assert branch_from_day(base_date) == Branch.PIG # 亥

    # Another known date (Result based on 2025-04-24 base date)
    known_date_1 = datetime.date(2000, 1, 1)
    assert branch_from_day(known_date_1) == Branch.HORSE # 午 (Expected Dragon with 2000-01-01 base)

    # Date after base date
    known_date_2 = datetime.date(2025, 4, 25)
    assert branch_from_day(known_date_2) == Branch.RAT # 子

    # Date before base date
    known_date_3 = datetime.date(2025, 4, 23)
    assert branch_from_day(known_date_3) == Branch.DOG # 戌
