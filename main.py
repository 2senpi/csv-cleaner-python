import pandas as pd


INPUT_FILE = "sample_messy_data.csv"
OUTPUT_FILE = "cleaned_output.csv"


def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def trim_whitespace(data: pd.DataFrame) -> pd.DataFrame:
    cleaned_data = data.copy()
    text_columns = cleaned_data.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_data[column] = cleaned_data[column].str.strip()

    return cleaned_data


def normalize_column_names(data: pd.DataFrame) -> pd.DataFrame:
    cleaned_data = data.copy()
    cleaned_data.columns = (
        cleaned_data.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return cleaned_data


def handle_missing_values(
    data: pd.DataFrame,
    strategy: str,
) -> pd.DataFrame:
    if strategy == "drop":
        return data.dropna()

    return data.fillna({
        "season_points": 0,
        "status": "Unknown",
    })


def clean_data(data: pd.DataFrame, missing_strategy: str) -> pd.DataFrame:
    cleaned_data = data.drop_duplicates().copy()
    cleaned_data = trim_whitespace(cleaned_data)
    cleaned_data = normalize_column_names(cleaned_data)
    cleaned_data = handle_missing_values(cleaned_data, missing_strategy)
    cleaned_data = cleaned_data.sort_values(
        by="season_points",
        ascending=False,
    )
    return cleaned_data.reset_index(drop=True)


def print_summary(
    original_data: pd.DataFrame,
    cleaned_data: pd.DataFrame,
) -> None:
    print("\nCleaning summary")
    print(f"Rows before: {original_data.shape[0]}")
    print(f"Rows after: {cleaned_data.shape[0]}")
    print(f"Duplicates removed: {original_data.duplicated().sum()}")
    print(f"Missing values detected: {original_data.isna().sum().sum()}")
    print(f"Columns processed: {original_data.shape[1]}")


def main() -> None:
    data = load_csv(INPUT_FILE)
    missing_strategy = input(
        'Do you want to "drop" or "fill" missing values? '
    ).strip().lower()

    if missing_strategy not in {"drop", "fill"}:
        print('Error: please enter either "drop" or "fill".')
        return

    cleaned_data = clean_data(data, missing_strategy)
    cleaned_data.to_csv(OUTPUT_FILE, index=False)

    print_summary(data, cleaned_data)
    print(f"Cleaned data saved as {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
