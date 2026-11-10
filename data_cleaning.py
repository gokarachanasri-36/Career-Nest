"""
CareerNest - Data Cleaning
Reads CareerNest_Dataset.xlsx, removes duplicate rows, trims text fields,
normalizes blank values, and exports clean_dataset.xlsx plus per-sheet CSVs.
Run: python data_cleaning.py
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "CareerNest_Dataset.xlsx"
OUTPUT = BASE_DIR / "clean_dataset.xlsx"
CSV_DIR = BASE_DIR / "dataset_csv"


def clean_workbook(input_path=INPUT, output_path=OUTPUT):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Dataset not found: {input_path.resolve()}")

    sheets = pd.read_excel(input_path, sheet_name=None)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(exist_ok=True)
    summary = []

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            before = len(df)
            df = df.copy()
            for col in df.select_dtypes(include=["object", "string"]).columns:
                df[col] = df[col].astype("string").str.strip()
                df[col] = df[col].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
            duplicates = int(df.duplicated().sum())
            df = df.drop_duplicates()
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            safe_name = str(sheet_name).lower().replace(" ", "_")
            safe_name = "".join(ch for ch in safe_name if ch.isalnum() or ch in "_") or "sheet"
            df.to_csv(CSV_DIR / f"{safe_name}.csv", index=False)
            summary.append({
                "Sheet": sheet_name,
                "Rows Before": before,
                "Rows After": len(df),
                "Duplicate Rows Removed": duplicates,
                "Missing Cells After Cleaning": int(df.isna().sum().sum()),
            })
        pd.DataFrame(summary).to_excel(writer, sheet_name="Cleaning Summary", index=False)

    print(f"Cleaned workbook saved to: {output_path.resolve()}")
    print(f"CSV files saved in: {CSV_DIR.resolve()}")

if __name__ == "__main__":
    clean_workbook()
