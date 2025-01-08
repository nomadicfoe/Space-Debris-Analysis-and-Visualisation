import pandas as pd

def load_and_summarize_data(file_path, dataset_name):
    """
    Load dataset and provide a quick summary.
    """
    print(f"--- Loading {dataset_name} Dataset ---")
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

    # Summary statistics
    print(f"\nSummary Statistics for {dataset_name}:")
    print(df.describe())

    # Missing values
    missing_vals = df.isnull().sum()
    print(f"\nMissing Values in {dataset_name}:")
    print(missing_vals[missing_vals > 0])

    # Data types
    print(f"\nData Types in {dataset_name}:")
    print(df.dtypes)

    print(f"\nLoaded {dataset_name} with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def preprocess_data(df, cols_to_drop=None, cols_to_impute=None, date_cols=None, categorical_cols=None, impute_strategy='mean'):
    """
    Perform preprocessing: drop columns, impute missing values, handle dates, and encode categorical features.
    """
    # Drop unnecessary columns
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop, errors='ignore')

    # Impute missing values
    if cols_to_impute:
        for col in cols_to_impute:
            if impute_strategy == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif impute_strategy == 'median':
                df[col] = df[col].fillna(df[col].median())
            elif impute_strategy == 'mode':
                df[col] = df[col].fillna(df[col].mode().iloc[0])

    # Convert date columns
    if date_cols:
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Encode categorical columns
    if categorical_cols:
        for col in categorical_cols:
            df[col] = df[col].astype('category')

    return df

def quality_and_integrity_check(df, dataset_name):
    """
    Perform quality and integrity checks on the dataset.
    """
    print(f"--- Quality and Integrity Check for {dataset_name} Dataset ---")

    # Check for null values
    total_nulls = df.isnull().sum().sum()
    print(f"Total null values: {total_nulls}")

    # Check data types
    print("\nData Types:")
    print(df.dtypes)

    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"\nNumber of duplicate rows: {duplicates}")

    # Display basic statistics for numerical columns
    print("\nBasic Statistics for Numerical Columns:")
    print(df.describe())

    # Display first few rows of the dataset
    print("\nFirst few rows of the dataset:")
    print(df.head())

    print("\n------------------------------------------------\n")
