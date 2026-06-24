from datetime import datetime

import holidays
import pandas as pd

FILE_PATH = "./data/CanAI Cafe 2023 Sales Information.xlsx"


# Set Season
def get_season(month):
    # Note: Can set start and end days too if want
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"


def main():
    df = pd.read_excel(FILE_PATH)
    df = df.dropna(how="any")  # temporary clean just for ease

    # Convert to datetime
    df["date"] = pd.to_datetime(
        df["Transaction Date"], format="%m/%d/%Y", errors="coerce"
    )

    # Extract components
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year

    # Day of the week (name)
    df["day_of_week"] = df["date"].dt.day_name()

    # Seasons
    df["season"] = df["month"].apply(get_season)

    # Holiday Flag
    ca_holidays = holidays.CA(years=2023)
    ca_holidays.append(
        {
            # "9-4-2023": "Easter Monday",
            "22-5-2023": "Victoria Day",
            "3-7-2023": "Canada Day (observed)",
            "30-9-2023": "Truth and Reconcillation Day",
            "9-10-2023": "Thanksgiving Day",
            # "26-12-2023": "Boxing Day",
        }
    )
    # Note there are two New Year's Day
    # Note could also do regional holidays but is very time consuming
    print(ca_holidays.items())

    df["is_holiday"] = df["date"].dt.date.isin(ca_holidays)

    # print(df)
    print(df[df["is_holiday"] == True])


if __name__ == "__main__":
    main()
