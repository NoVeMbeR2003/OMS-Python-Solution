
from pathlib import Path
import pandas as pd

# -----------------------------------------
# 1. Define folder paths
# -----------------------------------------

PROCESSED_FOLDER = Path("data/processed")
CLEANED_FOLDER = Path("data/cleaned")
QUARANTINE_FOLDER = Path("data/quarantine")

CLEANED_FOLDER.mkdir(parents=True, exist_ok=True)
QUARANTINE_FOLDER.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# 2. Define rules for each CSV file
# -----------------------------------------

NULL_RULES = {
    "customer_master.csv": {
        "required": ["customer_id"],
        "fill_unknown": ["gender"]
    },
    "order_items.csv": {
        "required": ["order_id", "product_id"],
        "fill_unknown": []
    },
    "ecommerce_sales.csv": {
        "required": [],
        "fill_unknown": []
    },
    "product_catalog.csv": {
        "required": [],
        "fill_unknown": []
    }
}


# -----------------------------------------
# 3. Load one processed CSV file
# -----------------------------------------

def load_data(file_path):
    df = pd.read_csv(file_path)

    print(f"Loaded: {file_path.name}")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

    return df


# -----------------------------------------
# 4. Check null values
# -----------------------------------------

def check_nulls(df, stage):
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]

    print(f"\nNull report - {stage}")

    if null_counts.empty:
        print("No null values found.")
    else:
        print(null_counts)

    return null_counts


# -----------------------------------------
# 5. Handle null values
# -----------------------------------------

def handle_nulls(df, rules, file_name):
    df = df.copy()

    required_columns = rules["required"]
    fill_columns = rules["fill_unknown"]

    # Validate that configured columns exist
    configured_columns = required_columns + fill_columns
    missing_columns = [
        column for column in configured_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing required rule columns: "
            f"{missing_columns}"
        )

    # Quarantine rows with nulls in required columns
    if required_columns:
        invalid_mask = df[required_columns].isna().any(axis=1)
    else:
        invalid_mask = pd.Series(False, index=df.index)

    quarantine_df = df.loc[invalid_mask].copy()
    clean_df = df.loc[~invalid_mask].copy()

    # Fill only explicitly configured columns
    for column in fill_columns:
        clean_df[column] = clean_df[column].fillna("Unknown")

    return clean_df, quarantine_df


# -----------------------------------------
# 6. Check duplicate rows
# -----------------------------------------

def check_duplicates(df):
    duplicate_count = int(df.duplicated().sum())

    print(f"Duplicate rows found: {duplicate_count}")

    return duplicate_count


# -----------------------------------------
# 7. Remove exact duplicate rows
# -----------------------------------------

def remove_duplicates(df):
    before_count = len(df)

    df = df.drop_duplicates().copy()

    removed_count = before_count - len(df)

    print(f"Duplicate rows removed: {removed_count}")

    return df


# -----------------------------------------
# 8. Save cleaned and quarantined data
# -----------------------------------------

def save_data(df, output_folder, file_name):
    output_path = output_folder / file_name
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")


# -----------------------------------------
# 9. Run the complete pipeline
# -----------------------------------------

def run_pipeline():
    if not PROCESSED_FOLDER.exists():
        raise FileNotFoundError(
            f"Input folder not found: {PROCESSED_FOLDER}"
        )

    csv_files = sorted(PROCESSED_FOLDER.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/processed/.")
        return

    print(f"Total CSV files found: {len(csv_files)}")

    for file_path in csv_files:
        file_name = file_path.name

        print("\n" + "=" * 50)
        print(f"Processing: {file_name}")
        print("=" * 50)

        if file_name not in NULL_RULES:
            print("No rules defined. Skipping this file.")
            continue

        try:
            # Load one file
            df = load_data(file_path)
            original_rows = len(df)

            # Inspect source data
            check_nulls(df, "Before cleaning")
            check_duplicates(df)

            # Apply null rules
            rules = NULL_RULES[file_name]
            clean_df, quarantine_df = handle_nulls(
                df, rules, file_name
            )

            # Save rows with missing required values separately
            if not quarantine_df.empty:
                quarantine_name = (
                    f"{file_path.stem}_quarantine.csv"
                )
                save_data(
                    quarantine_df,
                    QUARANTINE_FOLDER,
                    quarantine_name
                )

            # Remove exact duplicate rows from valid records
            clean_df = remove_duplicates(clean_df)

            # Verify after cleaning
            check_nulls(clean_df, "After cleaning")
            check_duplicates(clean_df)

            # Save the cleaned dataset
            save_data(clean_df, CLEANED_FOLDER, file_name)

            print(f"Original rows: {original_rows}")
            print(f"Cleaned rows: {len(clean_df)}")
            print(f"Quarantined rows: {len(quarantine_df)}")

        except Exception as error:
            print(f"Failed to process {file_name}: {error}")
            print("Continuing to the next file.")


if __name__ == "__main__":
    run_pipeline()
