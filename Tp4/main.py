import os
import pandas as pd

def main():
    file_path = "Data/data.csv"

    print("_" * 50)
    print("      TP04 - Docker Data Processing")
    print("_" * 50)

    if not s.path.exists(file_path):
        print(f"Error: Dataset not found at {file_path}")
        return

    try:
        df = pd.read_csv(file_path)

        print("\n1. Dataset loaded successfully!")
        print(f"Number of rows: {df.shape[0]}")
        print(f"Number of columns: {df.shape[1]}")

        print("\n2. Column names:")
        print(df.columns.tolist())

        print("\n3. Data types:")
        print(df.dtypes.to_string())

        print("\n4. Missing values per column:")
        print(df.isnull().sum().to_string())

        print("\n5. First 5 rows:")
        print(df.head().to_string())

        print("\n6. Descriptive statistics:")
        print(df.describe(include="all").to_string())

        print("\nData processing completed successfully!")

    except Exception as error:
        print(f"Error while processing dataset: {error}")
        raise

if __name__ == "__main__":
    main()
