import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# view first five and last five data points
course = pd.read_csv("./data/OEDI Course Overview Data.csv")
course["SIS Location Desc"] = course["SIS Location Desc"].replace("#NAME?", pd.NA)
print(course.head())
print(course.tail())

# general cleaning
print(course.shape)     # Rows and Columns
print(course.columns)   # All column names
print(course.info())    # Data types and nulls

course.isnull().sum()   # find all nulls
course = course.dropna() # drop rows with missing values

# view all unique campus descriptions for hybrid and online instruction modes
course_hybrid = course.loc[course['Instruction Mode Desc'] == 'Hybrid']
print(course_hybrid['Class Campus Desc'].unique())

course_online = course.loc[course["Instruction Mode Desc"] == 'Online Synchronous']
print(course_online["Class Campus Desc"].unique())

course_online = course.loc[course["Instruction Mode Desc"] == 'Online Asynchronous']
print(course_online["Class Campus Desc"].unique())

# view all courses that are coded as "off-grounds" and "online asynchronous"
course_off_async = course.loc[(course['Class Campus Desc'] == 'Off-Grounds') & (course['Instruction Mode Desc'] == 'Online Asynchronous')]

print(course_off_async)
# find all unique academic groups that label online async classes as "off-grounds"
print("Unique academic groups (async):")
print(course_off_async["Class Academic Group Desc"].unique())

course_off_sync = course.loc[(course['Class Campus Desc'] == 'Off-Grounds') & (course['Instruction Mode Desc'] == 'Online Synchronous')]

print(course_off_sync)
# find all academic departments that code online sync classes as "off-grounds"
print("Unique academic groups (sync):")
print(course_off_sync["Class Academic Group Desc"].unique())

# view all courses that are tagged as online and either online async or online sync
course_async = course.loc[(course['Class Campus Desc'] == 'Online') & (course['Instruction Mode Desc'] == 'Online Asynchronous')]
print(course_async)
# find all academic departments that code with online and online async
print("Unique academic groups (async):")
print(course_async["Class Academic Group Desc"].unique())

course_sync = course.loc[((course['Class Campus Desc'] == 'Online') & (course['Instruction Mode Desc'] == 'Online Synchronous'))]
print(course_sync)
# find all academic departments that code with online and online sync
print("Unique academic groups (sync):")
print(course_sync["Class Academic Group Desc"].unique())

def filter(campus, mode, label):
    df = course.loc[
        (course['Class Campus Desc'] == campus) &
        (course['Instruction Mode Desc'] == mode)
    ]
    print(df)
    print("Unique academic groups (" + label + "):")
    print(df["Class Academic Group Desc"].unique())
    print("\n")
    return df


course_async_scps = filter('SCPS Campus', 'Online Asynchronous', 'async and SCPS')
course_sync_scps = filter('SCPS Campus', 'Online Synchronous', 'sync and SCPS')
course_async_main = filter('Main Campus', 'Online Asynchronous', 'async and main')
course_sync_main = filter('Main Campus', 'Online Synchronous', 'sync and main')

course_hybrid_scps = filter('SCPS Campus', 'Hybrid', 'Hybrid and SCPS')
course_hybrid_main = filter('Main Campus', 'Hybrid', 'Hybrid and Main')
course_hybrid_online = filter('Online', 'Hybrid', 'Hybrid and Online')
course_hybrid_off = filter('Off-Grounds', 'Hybrid', 'Hybrid and Off-Grounds')


# Find out how many courses are tagged in the specific modalities

print("Off-Grounds + Online Asynchronous:", course_off_async.shape[0])
print("Off-Grounds + Online Synchronous:", course_off_sync.shape[0])

print("Online + Online Asynchronous:", course_async.shape[0])
print("Online + Online Synchronous:", course_sync.shape[0])




# make graph to show the distribution
# Add a new column to label each modality combination
course["Modality Combo"] = np.select(
    [
        (course['SIS Location Desc'] == 'On Grounds') & (course['Instruction Mode Desc'] == 'Online Asynchronous'),
        (course['SIS Location Desc'] == 'On Grounds') & (course['Instruction Mode Desc'] == 'Online Synchronous'),
        (course['Class Campus Desc'] == 'Off-Grounds') & (course['Instruction Mode Desc'] == 'Online Asynchronous'),
        (course['Class Campus Desc'] == 'Off-Grounds') & (course['Instruction Mode Desc'] == 'Online Synchronous'),
        (course['Class Campus Desc'] == 'Online') & (course['Instruction Mode Desc'] == 'Online Asynchronous'),
        (course['Class Campus Desc'] == 'Online') & (course['Instruction Mode Desc'] == 'Online Synchronous'),
    ],
    [
        'On-Grounds + Online Asynchronous',
        'On-Grounds + Online Synchronous',
        'Off-Grounds + Online Asynchronous',
        'Off-Grounds + Online Synchronous',
        'Online + Online Asynchronous',
        'Online + Online Synchronous'
    ],
    default='Other'
)

# Filter only rows with one of the 4 modality combos
filtered = course[course["Modality Combo"] != "Other"]

# Group by modality and academic group
grouped = filtered.groupby(["Modality Combo", "Class Academic Group Desc"]).size().reset_index(name='Count')

# Pivot to get modality combos on x-axis, academic groups as hue
plt.figure(figsize=(14, 8))
sns.barplot(data=grouped, x="Modality Combo", y="Count", hue="Class Academic Group Desc", palette="tab20")
plt.title("Class Campus Location and Instruction Mode Distribution by Academic Group")
plt.xlabel("Modality Combination")
plt.ylabel("Number of Courses")
plt.xticks(rotation=20)
plt.legend(title="Academic Group", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()