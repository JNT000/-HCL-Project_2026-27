# This script makes the practice dataset (fake students, not real people).
# Run it from the main project folder:  python Scripts/generate_raw_data.py

import numpy as np
import pandas as pd

np.random.seed(7)
n = 200

section = np.random.choice(["A", "B", "C", "D"], n)
gender = np.random.choice(["Male", "Female"], n, p=[0.6, 0.4])
attendance = np.clip(np.random.normal(76, 13, n), 35, 100).round(0)
study = np.clip(np.random.normal(3.2, 1.4, n), 0.3, 8).round(1)
ability = np.random.normal(0, 1, n)

def make_marks(extra):
    m = 24 + 0.28 * attendance + 4.2 * study + 8 * ability + extra + np.random.normal(0, 7, n)
    return np.clip(m, 5, 100).round(0)

maths = make_marks(-2)
science = make_marks(-4)
english = make_marks(2)
computer = make_marks(5)
assignment = np.clip(0.5 * maths + 0.5 * computer + np.random.normal(5, 8, n), 10, 100).round(0)

df = pd.DataFrame({
    "Student_ID": ["STU" + str(i).zfill(3) for i in range(1, n + 1)],
    "Section": section,
    "Gender": gender,
    "Attendance_Percentage": attendance,
    "Daily_Study_Hours": study,
    "Maths_Marks": maths,
    "Science_Marks": science,
    "English_Marks": english,
    "Computer_Marks": computer,
    "Assignment_Score": assignment,
})

# making every column object type so that I can put text in the number columns
df = df.astype(object)

# ---- adding mistakes on purpose ----
# missing values
for col, rows in [("Attendance_Percentage", [5, 41, 77, 120, 163]),
                  ("Daily_Study_Hours", [18, 90, 134]),
                  ("Maths_Marks", [12, 60, 150]),
                  ("Science_Marks", [33, 101]),
                  ("Assignment_Score", [8, 70, 185]),
                  ("Section", [25]),
                  ("Gender", [140])]:
    df.loc[rows, col] = np.nan

# impossible values
df.loc[9, "Attendance_Percentage"] = 125
df.loc[88, "Attendance_Percentage"] = -20
df.loc[44, "Daily_Study_Hours"] = 18
df.loc[170, "Daily_Study_Hours"] = -2
df.loc[27, "Maths_Marks"] = 150
df.loc[111, "English_Marks"] = -10
df.loc[65, "Computer_Marks"] = 999

# text inside number columns
df.loc[[3, 52, 99, 142], "Attendance_Percentage"] = ["82%", "65%", "91%", "58%"]
df.loc[[14, 73, 128], "Daily_Study_Hours"] = ["3 hrs", "2.5 hrs", "4 hrs"]
df.loc[[22, 96], "Maths_Marks"] = "absent"
df.loc[[57], "Science_Marks"] = "absent"
df.loc[[81], "Computer_Marks"] = "NA"

# different spellings / spaces / capital letters
df.loc[[2, 30, 66, 104], "Section"] = [" a", "B ", "c", " d "]
df.loc[[6, 35, 70, 109, 150], "Gender"] = ["M", "male", "F", "FEMALE", " female"]

# 3 exact duplicate rows
df = pd.concat([df, df.iloc[[15, 48, 130]]], ignore_index=True)

df.to_csv("Data/Raw_data/student_performance_raw.csv", index=False)
print("Raw file saved, shape =", df.shape)
