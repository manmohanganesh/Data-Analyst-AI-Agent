from pathlib import Path

import pandas as pd

BASE_DIR=Path(__file__).resolve().parent.parent
print(BASE_DIR)

RAW_DATA_PATH = BASE_DIR/ "data" / "raw"

def inspect_csv_files():
    csv_files=list(RAW_DATA_PATH.glob("*.csv"))
    for file_path in csv_files:
        print("\n"+"="*70)
        print(f"FILE:{file_path.name}")
        print("="*70)
        df = pd.read_csv(file_path)
        print(f"\n Shape : {df.shape}")
        print("\n Columns:")
        print(df.columns.tolist())
        print("\n Data types:")
        print(df.dtypes)
        print("\n Missing Values")
        print(df.isnull().sum())
        print("\n First 3 rows ")
        print(df.head(3))

if __name__ == "__main__":
    inspect_csv_files() 