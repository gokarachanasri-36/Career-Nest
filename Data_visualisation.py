"""
CareerNest - Data Visualisation
Creates charts from clean_dataset.xlsx using Matplotlib.
Run: python Data_visualisation.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR / "clean_dataset.xlsx"
OUT = BASE_DIR / "charts"

def save_bar(series, title, xlabel, ylabel, filename):
    plt.figure(figsize=(9, 5))
    series.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

def main():
    if not DATA.exists():
        raise FileNotFoundError("Run data_cleaning.py first to create clean_dataset.xlsx")
    OUT.mkdir(exist_ok=True)
    students = pd.read_excel(DATA, sheet_name="Students")
    jobs = pd.read_excel(DATA, sheet_name="Jobs")
    apps = pd.read_excel(DATA, sheet_name="Applications")
    resumes = pd.read_excel(DATA, sheet_name="Resumes")

    save_bar(students["Status"].value_counts(), "Students by Status",
             "Status", "Number of Students", "students_by_status.png")
    save_bar(jobs["Location"].value_counts(), "Jobs by Location",
             "Location", "Number of Jobs", "jobs_by_location.png")
    save_bar(apps["Status"].value_counts(), "Applications by Status",
             "Application Status", "Number of Applications", "applications_by_status.png")

    plt.figure(figsize=(8, 5))
    plt.hist(resumes["Resume Score"].dropna(), bins=8)
    plt.title("Distribution of Resume Scores")
    plt.xlabel("Resume Score")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(OUT / "resume_score_distribution.png", dpi=160)
    plt.close()
    print(f"Charts saved in: {OUT.resolve()}")

if __name__ == "__main__":
    main()
