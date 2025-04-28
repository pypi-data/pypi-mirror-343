import datetime
import argparse
from enum import Enum

class Language(Enum):
    KANJI = 'kanji'
    ENGLISH = 'english'
    EMOJI = 'emoji'

# Heavenly Stems (Jikkan)
class Stem(Enum):
    WOOD_YANG = ('甲', 'Wood Yang', '🌳🌞')
    WOOD_YIN = ('乙', 'Wood Yin', '🌿🌑')
    FIRE_YANG = ('丙', 'Fire Yang', '🔥🌞')
    FIRE_YIN = ('丁', 'Fire Yin', '🕯️🌑')
    EARTH_YANG = ('戊', 'Earth Yang', '⛰️🌞')
    EARTH_YIN = ('己', 'Earth Yin', '🌱🌑')
    METAL_YANG = ('庚', 'Metal Yang', '🔩🌞')
    METAL_YIN = ('辛', 'Metal Yin', '⚙️🌑')
    WATER_YANG = ('壬', 'Water Yang', '🌊🌞')
    WATER_YIN = ('癸', 'Water Yin', '💧🌑')

    def __init__(self, kanji: str, english: str, emoji: str):
        self._kanji = kanji
        self._english = english
        self._emoji = emoji

    def display(self, lang: Language) -> str:
        if lang == Language.KANJI:
            return self._kanji
        elif lang == Language.ENGLISH:
            return self._english
        else:
            raise ValueError("Unsupported language")

    def display_emoji(self) -> str:
        return self._emoji

# Earthly Branches (Eto)
class Branch(Enum):
    RAT = ('子', 'Rat', '🐀')
    OX = ('丑', 'Ox', '🐂')
    TIGER = ('寅', 'Tiger', '🐅')
    RABBIT = ('卯', 'Rabbit', '🐇')
    DRAGON = ('辰', 'Dragon', '🐉')
    SNAKE = ('巳', 'Snake', '🐍')
    HORSE = ('午', 'Horse', '🐎')
    GOAT = ('未', 'Goat', '🐐')
    MONKEY = ('申', 'Monkey', '🐒')
    ROOSTER = ('酉', 'Rooster', '🐓')
    DOG = ('戌', 'Dog', '🐕')
    PIG = ('亥', 'Pig', '🐖')

    def __init__(self, kanji: str, english: str, emoji: str):
        self._kanji = kanji
        self._english = english
        self._emoji = emoji

    def display(self, lang: Language) -> str:
        if lang == Language.KANJI:
            return self._kanji
        elif lang == Language.ENGLISH:
            return self._english
        else:
            raise ValueError("Unsupported language")

    def display_emoji(self) -> str:
        return self._emoji


# --- Calculation Functions ---

def branch_from_year(year: int) -> Branch: # Calculates Earthly Branch for the year
    branch_list = list(Branch)
    return branch_list[(year - 4) % 12]

def stem_from_year(year: int) -> Stem: # Calculates Heavenly Stem for the year
    stem_list = list(Stem)
    index_map = {4: 0, 5: 1, 6: 2, 7: 3, 8: 4, 9: 5, 0: 6, 1: 7, 2: 8, 3: 9}
    last_digit = year % 10
    return stem_list[index_map[last_digit]]


def branch_from_day(date: datetime.date) -> Branch: # Calculates Earthly Branch for the day
    branch_list = list(Branch)
    base_date = datetime.date(2025, 4, 24) # Base date: April 24, 2025 (Water Yin Pig)
    base_branch_index = 11 # Pig is the 11th Branch (0-indexed)
    delta = date - base_date
    days_diff = delta.days
    day_branch_index = (base_branch_index + days_diff) % 12
    return branch_list[day_branch_index]

def stem_from_day(date: datetime.date) -> Stem: # Calculates Heavenly Stem for the day
    stem_list = list(Stem)
    base_date = datetime.date(2025, 4, 24) # Base date: April 24, 2025 (Water Yin Pig)
    base_stem_index = 9 # Water Yin is the 9th Stem (0-indexed)
    delta = date - base_date
    days_diff = delta.days
    day_stem_index = (base_stem_index + days_diff) % 10
    return stem_list[day_stem_index]


def main():
    parser = argparse.ArgumentParser(description='Display the Heavenly Stem and Earthly Branch for the current date.') # Updated description
    parser.add_argument('--lang', type=str, choices=[lang.value for lang in Language],
                        default=Language.KANJI.value, help='Display language (kanji, english or emoji). Ignored if --format is used.')
    parser.add_argument('--format', type=str, default=None,
                        help='Custom output format string. Available variables: {year_stem_kanji}, {year_stem_english}, {year_stem_emoji}, {year_branch_kanji}, {year_branch_english}, {year_branch_emoji}, {day_stem_kanji}, {day_stem_english}, {day_stem_emoji}, {day_branch_kanji}, {day_branch_english}, {day_branch_emoji}, {date_kanji}, {date_english}') # Updated help text variables
    args = parser.parse_args()


    today = datetime.date.today()
    year = today.year

    # Calculate Stem and Branch for year and day
    year_stem = stem_from_year(year)
    year_branch = branch_from_year(year)
    day_stem = stem_from_day(today)
    day_branch = branch_from_day(today)

    if args.format:
        # Prepare variables for the format string
        template_vars = {
            'year_stem_kanji': year_stem.display(Language.KANJI),
            'year_stem_english': year_stem.display(Language.ENGLISH),
            'year_stem_emoji': year_stem.display_emoji(),
            'year_branch_kanji': year_branch.display(Language.KANJI),
            'year_branch_english': year_branch.display(Language.ENGLISH),
            'year_branch_emoji': year_branch.display_emoji(),
            'day_stem_kanji': day_stem.display(Language.KANJI),
            'day_stem_english': day_stem.display(Language.ENGLISH),
            'day_stem_emoji': day_stem.display_emoji(),
            'day_branch_kanji': day_branch.display(Language.KANJI),
            'day_branch_english': day_branch.display(Language.ENGLISH),
            'day_branch_emoji': day_branch.display_emoji(),
            'date_kanji': today.strftime('%Y年%m月%d日'),
            'date_english': today.strftime('%B %d, %Y'),
        }
        try:
            print(args.format.format(**template_vars))
        except KeyError as e:
            print(f"Error: Invalid variable in format string: {e}")
        except Exception as e:
            print(f"Error formatting output: {e}")
    else:
        # Default behavior using --lang
        lang = Language(args.lang)
        if lang == Language.KANJI:
            date_str = today.strftime('%Y年%m月%d日')
            # Combine Stem and Branch for display (Stem first)
            year_combined_str = f"{year_stem.display(lang)}{year_branch.display(lang)}"
            day_combined_str = f"{day_stem.display(lang)}{day_branch.display(lang)}"
            print(f"今日は {date_str} です。")
            print(f"今年の干支（年干支）は「{year_combined_str}」です。")
            print(f"今日の干支（日干支）は「{day_combined_str}」です。")
        elif lang == Language.ENGLISH:
            date_str = today.strftime('%B %d, %Y')
            # Combine Stem and Branch for display (Stem first) with slash
            year_combined_str = f"{year_stem.display(lang)} / {year_branch.display(lang)}"
            day_combined_str = f"{day_stem.display(lang)} / {day_branch.display(lang)}"
            print(f"Today is {date_str}.")
            print(f"The Stem/Branch for this year is '{year_combined_str}'.") # Updated label
            print(f"The Stem/Branch for this day is '{day_combined_str}'.") # Updated label
        elif lang == Language.EMOJI:
            # Combine Stem and Branch emojis (Stem first) with slash
            year_emoji_str = f"{year_stem.display_emoji()}/{year_branch.display_emoji()}"
            day_emoji_str = f"{day_stem.display_emoji()}/{day_branch.display_emoji()}"
            print(f"Year: {year_emoji_str}")
            print(f"Day: {day_emoji_str}")
# (No changes needed below this line for the swap itself,
# but the variable names and logic inside main() were updated above)

if __name__ == "__main__":
    main()
