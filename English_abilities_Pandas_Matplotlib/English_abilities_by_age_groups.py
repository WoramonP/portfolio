"""
This project mainly uses NumPy, Pandas and Matplotlib to answer the research question:
In year 2000, did US population from different age groups have different English language abilities?

Data comes from the US Census: https://www2.census.gov/programs-surveys/decennial/2000/phc/phc-t-20
specifically Table 2 for Population 5 to 17 Years and Table 3 for Population 18 Years and Over.

Author: Woramon P.
Date: 9/4/22
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read two data files, one for population 5 to 17 years old, the other for population 18 years old and over
df_517 = pd.read_excel('language_5_to_17.xls', header=[5, 6, 7], nrows=1)  # Table 2 from the Census
df_18 = pd.read_excel('language_18_and_over.xls', header=[5, 6, 7], nrows=1)  # Table 3 from the Census
df = pd.concat([df_517, df_18], join='outer')

# manipulate the data frame: rename index and filter for data to be used
df.index = ['5 to 17', '18 and over']
df = df[[('Speak only English', 'Unnamed: 2_level_1', 'Unnamed: 2_level_2'),
         ('Speak non-English language at home', 'Speak English', '"Very well"'),
         ('Speak non-English language at home', 'Speak English', '"Well"'),
         ('Speak non-English language at home', 'Speak English', '"Not well"'),
         ('Speak non-English language at home', 'Speak English', '"Not at all"')]]
df.columns = ['Eng_only', 'Eng_very_well', 'Eng_well', 'Eng_not_well', 'Eng_not_at_all']
df = df.T
print(df)

# calculate percentage of people in each category
df['5 to 17 pct'] = round(df['5 to 17'] / df['5 to 17'].sum() * 100, 2)
df['18 and over pct'] = round(df['18 and over'] / df['18 and over'].sum() * 100, 2)
print(df)
df = df[['5 to 17 pct', '18 and over pct']]

# see pre-defined plot styles
# print(plt.style.available)

# draw bar plot
plt.style.use('seaborn-colorblind')
fig = plt.figure(figsize=(6, 8))
ax = plt.gca()
labels = {'Eng_only': 'Speak English only',
          'Eng_very_well': 'Speak non-English & Speak English very well',
          'Eng_well': 'Speak non-English & Speak English well',
          'Eng_not_well': 'Speak non-English & Don\'t speak English well',
          'Eng_not_at_all': 'Speak non-English & Don\'t speak English at all'}
bottom_bars = np.array([0, 0])  # used to calculate location of stacked bars
for idx in df.index:
    bar = ax.bar(df.columns, df.loc[idx], bottom=bottom_bars, label=labels[idx])
    bottom_bars += df.loc[idx]
    # give the top bar label a padding because it is small and hard to read when the number is on top of the bar
    ax.bar_label(bar, label_type='center', size=11, padding=8 if idx == 'Eng_not_at_all' else 0)

ax.set_title('Percentage of US population with different\nEnglish abilities in year 2000', fontsize=16)
ax.set_ylabel('Percentage', fontsize=16)
ax.set_xlabel('Age group', fontsize=16)
ax.set_xticks([0, 1], labels=['5 to 17 years old', '18 years and over'])

# edit plot for aesthetics
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(bottom=False, left=False, labelleft=False)

# provide legend in reverse order, so that it matches the order of the bars
# https://matplotlib.org/1.3.1/users/legend_guide.html
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles[::-1], labels[::-1], loc='lower center')
plt.show()
