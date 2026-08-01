import pandas as pd
import numpy as np


df = pd.read_csv('/Users/bakulseth/PycharmProjects/learning/data/raw/olympic/2022/olympic_athletes.csv')

# print(df.head(5))
# df.info()

# print(df.describe())
# print(df.shape)

df_subset = df[['athlete_url', 'athlete_full_name']]
# print(df_subset.head(5))
# # print(df_subset.shape)

df_filtered = df[df['games_participations'] > 2][['athlete_full_name', 'games_participations']]
# print(df_filtered.head(5))
# print(df_filtered.shape)

# 1. Paste this block to build your mock dataset
raw_data = {
    'employee_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Henry'],
    'department': ['Engineering', 'Sales', 'Engineering', 'Marketing', 'Sales', 'Engineering', 'Marketing', 'Sales'],
    'salary': [85000, 60000, np.nan, 55000, 62000, 95000, np.nan, 58000],
    'experience_years': [2, 4, 1, 1, 4, 3, 6, 1],
    'country': ['UK', 'USA', 'UK', 'USA', 'UK', 'USA', 'UK', 'UK']
}

df = pd.DataFrame(raw_data)
print("--- Sandbox DataFrame Loaded ---")
print(df)

df.info()
print(df.describe())
print(df.isnull().sum())

missing_salary_df = df[df['salary'].isna()]
print(missing_salary_df)
avg_salary = df['salary'].mean()
print(avg_salary)
df['salary'] = df['salary'].fillna(df['salary'].mean())
print(df)
print(df[(df['country'] == 'UK') & (df['experience_years'] > 3)])
print(df.groupby('department').agg(avg_salary=('salary', 'mean'), emp_count=('employee_id', 'count')))
df['seniority'] = np.where(df['experience_years'] >= 4, 'Senior', 'Junior')
print(df)