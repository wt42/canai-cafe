import pandas as pd
from dataset_cleaner import clean_province, standardize_items

FILE_PATH = "./data/CanAI Cafe 2023 Sales Information.xlsx"


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def normalize_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def print_value_counts(title, values):
    print_section(title)
    print(values.value_counts(dropna=False).sort_index())


def main():
    df = pd.read_excel(FILE_PATH)

    # Item Column Values
    print_value_counts(
        "Raw Unique Item Names",
        df["Item"].map(normalize_text),
    )
    print_value_counts(
        "Standardized Unique Item Names",
        standardize_items(df["Item"]),
    )

    # Province Column Values
    print_value_counts(
        "Raw Unique Province Names",
        df["Province"].map(normalize_text),
    )
    print_value_counts(
        "Standardized Unique Province Names",
        clean_province(df["Province"]),
    )

    # Payment Method Column Values
    print_value_counts(
        "Raw Unique Payment Methods",
        df["Payment Method"].map(normalize_text),
    )

    # Location Column Values
    print_value_counts(
        "Raw Unique Locations",
        df["Location"].map(normalize_text),
    )


if __name__ == "__main__":
    main()
