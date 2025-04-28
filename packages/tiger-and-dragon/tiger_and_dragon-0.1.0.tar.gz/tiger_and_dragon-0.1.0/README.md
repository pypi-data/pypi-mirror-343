# Tiger and Dragon (Stem/Branch Calculator)

A Python script to calculate and display the Heavenly Stem (Jikkan) and Earthly Branch (Eto/Junishi) for a given date.

## Features

*   Calculates the Stem/Branch combination for a given year.
*   Calculates the Stem/Branch combination for a given day.
*   Supports output in Japanese (Kanji), English, or Emoji.
*   Allows custom output formatting using template strings.

## Installation

1.  Clone the repository.
2.  Install dependencies using [uv](https://github.com/astral-sh/uv) (`pytest` is required for running tests).

    ```bash
    uv sync --dev
    ```

## Usage

Run the script from the command line:

```bash
python main.py [options]
```

### Options

*   `--lang {kanji,english,emoji}`: Specify the output language. Default is `kanji`. (Ignored if `--format` is used)
    *   `kanji`: Display in Japanese Kanji (e.g., 甲子)
    *   `english`: Display in English (e.g., Wood Yang / Rat)
    *   `emoji`: Display using emojis (e.g., 🌳🌞/🐀)
*   `--format FORMAT_STRING`: Specify a custom output format using a template string. This option overrides `--lang`.
    Available variables:
    *   `{year_stem_kanji}`, `{year_stem_english}`, `{year_stem_emoji}`
    *   `{year_branch_kanji}`, `{year_branch_english}`, `{year_branch_emoji}`
    *   `{day_stem_kanji}`, `{day_stem_english}`, `{day_stem_emoji}`
    *   `{day_branch_kanji}`, `{day_branch_english}`, `{day_branch_emoji}`
    *   `{date_kanji}`, `{date_english}`

### Examples

*   Display in default language (Kanji):
    ```bash
    python main.py
    ```
*   Display in English:
    ```bash
    python main.py --lang english
    ```
*   Display using emojis:
    ```bash
    python main.py --lang emoji
    ```
*   Display using a custom format:
    ```bash
    python main.py --format "Date: {date_english}, Year: {year_stem_english}/{year_branch_english} ({year_stem_emoji}/{year_branch_emoji}), Day: {day_stem_english}/{day_branch_english} ({day_stem_emoji}/{day_branch_emoji})"
    ```
    ```bash
    # Example with Japanese date and combined emoji/kanji
    python main.py --format "Date (Kanji): {date_kanji}, Day Stem/Branch: {day_stem_emoji}{day_branch_emoji} ({day_stem_kanji}{day_branch_kanji})"
    ```

## Using as a Library

You can import functions from `main.py` into other Python scripts.

```python
# example.py
import datetime
from main import stem_from_day, branch_from_day, Stem, Branch, Language

target_date = datetime.date(2024, 12, 25)

# Get the day's Stem
day_stem = stem_from_day(target_date)
# Get the day's Branch
day_branch = branch_from_day(target_date)

print(f"Date: {target_date}")
print(f"Day Stem (Kanji): {day_stem.display(Language.KANJI)}")
print(f"Day Branch (English): {day_branch.display(Language.ENGLISH)}")
print(f"Day Stem/Branch (Emoji): {day_stem.display_emoji()}/{day_branch.display_emoji()}")
```

## Testing

Run tests using `pytest`.

```bash
uv run pytest -v
