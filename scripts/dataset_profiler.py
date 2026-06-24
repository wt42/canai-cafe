import pandas as pd


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


def main():
    df = pd.read_excel(FILE_PATH)

    print_section("Raw Unique Item Names")
    item_values = (
        df["Item"]
        .map(normalize_text)
        .value_counts(dropna=False)
        .sort_index()
    )
    print(item_values)

    print_section("Raw Unique Province Names")
    province_values = (
        df["Province"]
        .map(normalize_text)
        .value_counts(dropna=False)
        .sort_index()
    )
    print(province_values)

    print_section("Raw Unique Payment Methods")
    payment_values = (
        df["Payment Method"]
        .map(normalize_text)
        .value_counts(dropna=False)
        .sort_index()
    )
    print(payment_values)

    print_section("Raw Unique Locations")
    location_values = (
        df["Location"]
        .map(normalize_text)
        .value_counts(dropna=False)
        .sort_index()
    )
    print(location_values)

if __name__ == "__main__":
    main()

