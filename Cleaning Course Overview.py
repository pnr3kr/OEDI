import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# view first five and last five data points
course = pd.read_csv("OEDI Course Overview Data.csv")
print(course.head())
print(course.tail())

# general cleaning
print(course.shape)     # Rows and Columns
print(course.columns)   # All column names
print(course.info())    # Data types and nulls

course.isnull().sum()   # find all nulls
course = course.dropna() # drop rows with missing values

# view all courses that are coded as "off-grounds" and "online" to see inconsistencies in modalities
course_off_async = course.loc[(course['Class Campus Desc'] == 'Off-Grounds') & (course['Instruction Mode Desc'] == 'Online Asynchronous')]

print(course_off_async)
# find all unique academic groups that label online async classes as "off-grounds"
print("Unique academic groups (async):")
print(course_off_async["Class Academic Group"].unique())

course_off_sync = course.loc[(course['Class Campus Desc'] == 'Off-Grounds') & (course['Instruction Mode Desc'] == 'Online Synchronous')]

print(course_off_sync)
# find all academic departments that code online sync classes as "off-grounds"
print("Unique academic groups (sync):")
print(course_off_sync["Class Academic Group"].unique())

# view all courses that are tagged as online and either online async or online sync
course_async = course.loc[(course['Class Campus Desc'] == 'Online') & (course['Instruction Mode Desc'] == 'Online Asynchronous')]
print(course_async)
# find all academic departments that code with online and online async
print("Unique academic groups (async):")
print(course_async["Class Academic Group"].unique())

course_sync = course.loc[((course['Class Campus Desc'] == 'Online') & (course['Instruction Mode Desc'] == 'Online Synchronous'))]
print(course_sync)
# find all academic departments that code with online and online sync
print("Unique academic groups (sync):")
print(course_sync["Class Academic Group"].unique())


# Find out how many courses are tagged in the specific modalities

print("Off-Grounds + Online Asynchronous:", course_off_async.shape[0])
print("Off-Grounds + Online Synchronous:", course_off_sync.shape[0])

print("Online + Online Asynchronous:", course_async.shape[0])
print("Online + Online Synchronous:", course_sync.shape[0])