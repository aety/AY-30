import pandas as pd
import seaborn as sns
import matplotlib
from datetime import datetime
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

# format plots
register_matplotlib_converters()
sns.set_context("talk")
sns.set_style("dark")

# load data
filename = 'AY_30.xlsx'
data = pd.read_excel(filename)
data = data.rename(columns={'Year-we-met': 'Year met', 'Date': 'Reply date'})

# convert to datetime
data['Reply date'] = pd.to_datetime(data['Reply date'])

# count lengths of texts
df = pd.DataFrame()
breakdown = ['greetings', 'story', 'advice', 'others']
for number, column in enumerate(breakdown):
    one_series = data['Breakdown-' + column].fillna('')
    data.loc[:, column] = one_series.apply(len)
    data.loc[:, 'Reply'] = data.index
    df_sub = data.loc[:, ['Reply', column]]
    df_sub.loc[:, 'length'] = df_sub.loc[:, column]
    df_sub.loc[:, 'theme'] = [column]*(len(df_sub))
    df_sub = df_sub.loc[:, ['Reply', 'length', 'theme']]
    df = df.append(df_sub)

plt.figure(figsize=(10, 3))
g = sns.barplot(data=df, x='Reply', y='length', hue='theme')
g.legend(loc='best', ncol=4)
plt.tight_layout()
plt.savefig('lengths.jpg')
plt.close()

# plot counts
data['Total length'] = data['greetings'] + data['story'] + data['advice'] + data['others']
columns = ['Source', 'Country', 'Language', 'Year met', 'Reply date']
for n, column in enumerate(columns):
    print(column)
    plt.figure(figsize=(5, 3))
    values = data.groupby(column).count()['Name']
    plt.bar(values.index, values, facecolor='0.25', edgecolor='0.25')
    plt.xticks(rotation=45)
    plt.xlabel(column)
    plt.tight_layout()
    plt.savefig('frequency_' + str(n) + '.jpg')
    plt.close()    

# plot total text lengths
column = 'Total length'
plt.figure(figsize=(5, 3))
values = data[column]
plt.hist(values, bins=len(values), color='0.25')
plt.xlabel(column)
plt.tight_layout()
plt.savefig('hist.jpg')
plt.close()

data.to_json('AY_30_proc.json')

