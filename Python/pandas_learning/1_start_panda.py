import pandas as pd

# print(pd.__version__)

# Create Dataframe
df = pd.DataFrame([11, 22, 33], columns=['col_name'])
# print(df)
# print(type(df))
# print(df.dtypes)
# print(df.shape)


data = {
    'Name': ['Madhav', 'Vishakha', 'Lalita', 'Rishabh'],
    'Age': [16,17,18,19],
    'Salary': [90000, 70000, 50000, 30000]
}

df1 = pd.DataFrame(data)
# print(df1)
# print(df1.head())
# print(df1.tail())
# print(df1.columns)
# print(df1.rename(columns={"Salary": "monthly_salary"}, inplace=True))
# print(df1)
# print(df1.info())
# print(df1.describe())


# df1.to_csv("test_data.csv", index=False)
emp_path = "/Users/bakulseth/PycharmProjects/learning/Python/pandas_learning/test_data.csv"
emp_df = pd.read_csv(emp_path)
print(emp_df)

# 4. row column selection
# print(emp_df[['Name', 'Salary']])
#
# print(emp_df.loc[emp_df.Name=='Madhav'])
# print(emp_df.loc[emp_df.Age>17])
#
# print(emp_df.iloc[0:2])
# print(emp_df.loc[0:3])

# 5 filter rows
print(emp_df[emp_df['Age'] > 17])

print(emp_df[(emp_df['Age'] > 16) & (emp_df['Salary'] > 35000)])

print(emp_df.where(emp_df['Age'] > 17))

# Add new columns
emp_df['Team'] = ['CEO', 'HR', 'CTO', 'DA']
print(emp_df)
emp_df['Bonus'] = emp_df['Salary'] * .2
print(emp_df)

