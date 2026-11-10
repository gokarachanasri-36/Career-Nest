"""
CareerNest - Data Analysis
Creates descriptive summaries and CSV/Excel outputs from the cleaned workbook.
Run: python Data_analysis.py
"""
from pathlib import Path
import pandas as pd

DATA = Path("clean_dataset.xlsx")

def main():
    if not DATA.exists():
        raise FileNotFoundError("Run data_cleaning.py first to create clean_dataset.xlsx")
    students = pd.read_excel(DATA, sheet_name="Students")
    jobs = pd.read_excel(DATA, sheet_name="Jobs")
    applications = pd.read_excel(DATA, sheet_name="Applications")
    resumes = pd.read_excel(DATA, sheet_name="Resumes")

    summaries = {
        "Student Status": students["Status"].value_counts(dropna=False).rename_axis("Status").reset_index(name="Count"),
        "Preferred Jobs": students["Preferred Job"].value_counts().rename_axis("Preferred Job").reset_index(name="Students"),
        "Job Locations": jobs["Location"].value_counts().rename_axis("Location").reset_index(name="Job Count"),
        "Application Status": applications["Status"].value_counts(dropna=False).rename_axis("Status").reset_index(name="Applications"),
        "Resume Scores": resumes[["Resume Score", "Profile Completion"]].describe().reset_index()
    }
    with pd.ExcelWriter("CareerNest_Analysis.xlsx", engine="openpyxl") as writer:
        for name, table in summaries.items():
            table.to_excel(writer, sheet_name=name[:31], index=False)
    for name, table in summaries.items():
        table.to_csv(f"analysis_{name.lower().replace(' ', '_')}.csv", index=False)

    print("Students:", len(students))
    print("Jobs:", len(jobs))
    print("Applications:", len(applications))
    print("Average resume score:", round(resumes["Resume Score"].mean(), 2))
    print("Analysis saved to CareerNest_Analysis.xlsx and CSV files.")

if __name__ == "__main__":
    main()
