"""
CareerNest - Clean Dataset Export
A simple reusable script to create clean student data in CSV and Excel formats.
Run: python clean_dataset.py
"""
from pathlib import Path
import pandas as pd

SOURCE = Path("CareerNest_Dataset.xlsx")

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Place {SOURCE.name} in this folder first.")
    students = pd.read_excel(SOURCE, sheet_name="Students")
    students = students.drop_duplicates().copy()
    for col in students.select_dtypes(include=["object"]).columns:
        students[col] = students[col].astype("string").str.strip()
        students[col] = students[col].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
    students.to_csv("CareerNest_Students_Clean.csv", index=False)
    students.to_excel("CareerNest_Students_Clean.xlsx", index=False)
    print("Created CareerNest_Students_Clean.csv and .xlsx")

if __name__ == "__main__":
    main()
