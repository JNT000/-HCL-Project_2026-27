# Same cleaning steps as in the notebook, but in one file.
# Run from the main project folder:  python Scripts/clean_data.py

import pandas as pd
import numpy as np

df = pd.read_csv("Data/Raw_data/student_performance_raw.csv")
print("Raw shape:", df.shape)

# remove duplicate rows
df = df.drop_duplicates().copy()

# text columns
df["Section"] = df["Section"].str.strip().str.upper()
gender_map = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}
df["Gender"] = df["Gender"].str.strip().str.lower().map(gender_map)

# number columns
df["Attendance_Percentage"] = df["Attendance_Percentage"].astype(str).str.replace("%", "", regex=False)
df["Daily_Study_Hours"] = df["Daily_Study_Hours"].astype(str).str.replace("hrs", "", regex=False)

number_cols = ["Attendance_Percentage", "Daily_Study_Hours", "Maths_Marks", "Science_Marks",
               "English_Marks", "Computer_Marks", "Assignment_Score"]
for col in number_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# impossible values become missing
df.loc[~df["Attendance_Percentage"].between(0, 100), "Attendance_Percentage"] = np.nan
df.loc[~df["Daily_Study_Hours"].between(0, 12), "Daily_Study_Hours"] = np.nan
for col in ["Maths_Marks", "Science_Marks", "English_Marks", "Computer_Marks", "Assignment_Score"]:
    df.loc[~df[col].between(0, 100), col] = np.nan

# fill missing values
for col in number_cols:
    df[col] = df[col].fillna(df[col].median())
df["Section"] = df["Section"].fillna(df["Section"].mode()[0])
df["Gender"] = df["Gender"].fillna(df["Gender"].mode()[0])

# new columns
subjects = ["Maths_Marks", "Science_Marks", "English_Marks", "Computer_Marks"]
df["Total_Marks"] = df[subjects].sum(axis=1)
df["Average_Marks"] = (df["Total_Marks"] / 4).round(2)
df["Result"] = np.where((df[subjects] >= 40).all(axis=1), "Pass", "Fail")
df["Attendance_Group"] = pd.cut(df["Attendance_Percentage"], bins=[0, 70, 85, 100],
                                labels=["Below 70%", "70-85%", "Above 85%"], include_lowest=True)
df["Study_Group"] = pd.cut(df["Daily_Study_Hours"], bins=[0, 2, 4, 12],
                           labels=["Below 2 hrs", "2-4 hrs", "Above 4 hrs"], include_lowest=True)

df.to_csv("Data/Clean_data/student_performance_clean.csv", index=False)
print("Clean shape:", df.shape)
print("Missing values left:", df.isnull().sum().sum())
