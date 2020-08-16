import pandas as pd
import seaborn as sns
import matplotlib
from datetime import datetime
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

# format plots
register_matplotlib_converters()
font = {'family' : 'sans-serif',
	'sans-serif' : ['Helvetica'],
        'weight' : 'normal',
        'size'   : 12}
matplotlib.rc('font', **font)

# load data
filename = 'AY_30.xlsx'
data = pd.read_excel(filename)
data = data.rename(columns={'Year-we-met': 'Year met', 'Date': 'Reply date'})

# convert to datetime
data['Reply date'] = pd.to_datetime(data['Reply date'])



# plot counts
columns = ['Source', 'Country', 'Language']
for n, column in enumerate(columns):
    plt.figure(figsize=(6, 4))
    g = sns.countplot(x=column, data=data, color='0.5')
    plt.tight_layout()
    plt.savefig('AY_30_frequency_' + str(n) + '.jpg')
    plt.close()

# plot time-related counts
columns = ['Year met', 'Reply date']
for n, column in enumerate(columns):
    plt.figure(figsize=(6, 4))
    values = data.groupby(column).count()['Name']
    plt.bar(values.index, values, color='0.5')
    plt.xticks(rotation=45)
    plt.xlabel(column)
    plt.tight_layout()
    plt.savefig('AY_30_frequency_' + str(3 + n) + '.jpg')
    plt.close()    


# count lengths of texts
df = pd.DataFrame()
breakdown = ['greetings', 'story', 'advice', 'others']
for number, column in enumerate(breakdown):
    one_series = data['Breakdown-' + column].fillna('')
    data.loc[:, column] = one_series.apply(len)
    data.loc[:, 'Indexes'] = data.index
    df_sub = data.loc[:, ['Indexes', column]]
    df_sub.loc[:, 'length'] = df_sub.loc[:, column]
    df_sub.loc[:, 'label'] = [column]*(len(df_sub))
    df_sub = df_sub.loc[:, ['Indexes', 'length', 'label']]
    df = df.append(df_sub)

plt.figure(figsize=(6, 4))
sns.catplot(data=df, x='Indexes', y='length', hue='label', kind='bar')
plt.savefig('lengths.jpg')
plt.close()
