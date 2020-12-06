import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime


# Creating Graphs

os.getcwd()
path_with_os = os.path.expanduser(r'~\Documents\GitHub\Nadia-and-Yuwen-final-project')
file1 = os.path.join(path_with_os, 'data.csv')
df = pd.read_csv(file1, header=0)
df.dtypes

#change to datetime format
df['date'] = pd.to_datetime(df['date'])
df['policy_date'] = pd.to_datetime(df['policy_date'])
df.dtypes




# 1) Average Comparison of The Number of Cases between Republican and Democrat States
df['tot_avg_party'] = df.groupby(['date', 'party'])['positive'].transform('mean')
df['new_cases'] = df.groupby(['state_name'])['positive'].diff(-1)
df['positive_by_date'] = df.groupby(['date'])['positive'].transform('sum')
df['death_by_date'] = df.groupby(['date'])['death'].transform('sum')
df['new_case_mean_party'] = df.groupby(['date', 'party'])['new_cases'].transform('mean')
df['new_case_total'] = df.groupby(['date'])['new_cases'].transform('mean')
df['after_policy'] = (df['date'] > df['policy_date']).astype(int)
df['new_case_after'] = df.groupby(['state_name', 'after_policy'])['new_cases'].transform('mean')

# Inspired from: https://stackoverflow.com/questions/35599607/average-date-array-calculation
mean_reopening = (np.array(df['policy_date'], dtype='datetime64[ns]')
                  .view('i8')
                  .mean()
                  .astype('datetime64[ns]'))

# Add bar chart for average daily cases overall
def plot_cases_by_party(data, fname):
    fig, ax = plt.subplots(figsize=(15,7))
    ax.set_title('Average Number of Covid-19 Daily Cases', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('New Cases', fontsize=14)
    ax.bar('date', 'new_case_total', data = data, color='lightgray')
    dstart = datetime(2020,4,1)
    dend = datetime(2020,11,30)
    ax.set_xlim(dstart, dend)
    ax2 = ax.twinx()
    ax2 = sns.lineplot(x='date', y='new_case_mean_party', hue='party', data = data, palette=['r', 'b'])
    ax2.set_yticks([])
    ax2.set_ylabel('')
    ax2.axvline(datetime(2020,5,16), color='k', linestyle='--')
    legend = ax2.legend(loc='best')
    legend.texts[0].set_text('Political Party')
    plt.savefig(fname)
    plt.show()
    
plot_cases_by_party(df, 'average_by_party.png')

# 2) Show bar chart by state with highest average number of Covid-19 cases after reopening
df_overall = df[['state_name', 'new_case_after', 'after_policy', 'party']].drop_duplicates()
df_overall = df_overall[df_overall['after_policy']==1].nlargest(25, 'new_case_after')

def bar_by_party(data, fname):
    fig, ax = plt.subplots(figsize=(15,8))
    ax.set_title('Average Number of Daily Cases of 25 States with Highest Cases after Reopening', fontsize=16)
    ax.set_xlabel('Total Cases', fontsize=14)
    ax.set_ylabel('State', fontsize=14)
    y_pos = np.arange(len(df_overall['state_name']))
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_overall['state_name'])
    ax.invert_yaxis()
    
    top25_state = [r for r in df_overall['state_name']]
    top25_party = [r for r in df_overall['party']]
    top25_dict = {k:v for k,v in zip(top25_state, top25_party)}

    clr = []
    for v in top25_dict.values(): # keys are the names of the boys
        if v == 'republican':
            clr.append('indianred')
        else:
            clr.append('darkblue')
            
    ax.barh(y_pos, data['new_case_after'], color=clr, align='center')
    red_patch = mpatches.Patch(color='indianred', label='Republican')
    blue_patch = mpatches.Patch(color='darkblue', label='Democrat')
    plt.legend(handles=[red_patch, blue_patch])
    plt.savefig(fname)
    plt.show()

bar_by_party(df_overall, 'top25_states_highest_cases.png')







# 3) & 4) get the top 5 and bottom 5 states
# get data before Nov.30
df = df[df['date'] <= '2020-11-30']


#get the number of case increase per day for each state
df['dif'] = df.groupby('state_name')['positive'].diff(-1)


#select case increase data after reopen date
after_reopen = df[df['date'] >= df['policy_date']]

#calculate the daily avg # of new cases for each state
avg_case_increase =  after_reopen.groupby('state_name')['dif'].mean().reset_index()

#get the top 5 and bottom 5 states

low_5 = avg_case_increase.sort_values('dif').head(5)['state_name'].tolist()
top_5 = avg_case_increase.sort_values('dif').tail(5)['state_name'].tolist()
low_string = "The 5 states with lowest avg daily new cases are {}".format(', '.join([str(elem) for elem in low_5]))
high_string = "The 5 states with highest avg daily new cases are {}".format(', '.join([str(elem) for elem in top_5]))
print(high_string)
print(low_string)

#add list characterstics in the list
#will be used in the plot title
low_5.append(low_string[0:44])
top_5.append(high_string[0:45])

#draw plots and put them together
def plot_together(which_states):
    
    fig, axs = plt.subplots(5, figsize=(80,60))
    
    #set legend
    red_patch = mpatches.Patch(color='red', label='Republican')
    blue_patch = mpatches.Patch(color='blue', label='Democrat')
    fig.legend(handles=[red_patch, blue_patch], fontsize = 40)

    #generate plot by state and put rogether
    for i, ax in enumerate(axs):
        state = which_states[i]
        data = df[df['state_name'] == state].reset_index().sort_values('date')
        if data['party'][0] == 'republican':
            color = 'red'
        else:
            color = 'blue'
        date = data['policy_date'][0]
        ax.bar('date', 'dif', color = color, data = data)
        ax.axvline(x=date, color ='k', ymin=0, linewidth = 4)
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 27))
        ax.tick_params(axis='x', labelsize=25)
        ax.tick_params(axis='y', labelsize=25)
        ax.text(date, ax.get_ylim()[1]+0.0001, 'Reopen date', horizontalalignment='center', style='italic', fontsize = 30)
        ax.set_ylabel('New Cases')
        ax.set_xlabel('')
        ax.set_title('Number of daily new cases in {}'.format(state), fontsize = 30);
    
    fig.tight_layout()

    #give a general title 
    fig.text(0.43, 1.01, '{}'.format(which_states[5]), va='center', fontsize = 40)
    

    png_path = os.path.join(path_with_os, '{}.png'.format(which_states[5]))
    plt.savefig(png_path, bbox_inches='tight') #add "bbox_inches='tight'" to avoid cutoff title
    print('Image saved: ', png_path)
    plt.show()

#draw graph for 5 states with the highest average daily new cases
plot_together(top_5)
#draw graph for 5 states with the lowest average daily new cases
plot_together(low_5)








# 5) Before and After estimation
# Subset dataframe
df_ba = df[['date', 'positive_by_date', 'death_by_date']].drop_duplicates()
df_ba['month_year'] = pd.to_datetime(df_ba['date']).dt.to_period('M')
df_ba['month_year'] = df_ba['month_year'].dt.strftime('%Y-%m-%d')
df_ba['after'] = (df['date'] > mean_reopening).astype(int)
df_ba['new_case_by_date'] = df_ba['positive_by_date'].diff(-1)
df_ba['new_case_avg'] = df_ba.groupby(['after'])['new_case_by_date'].transform('mean')

df_ba['positive_by_month'] = df_ba.groupby(['month_year'])['positive_by_date'].transform('mean')
df_ba['death_by_month'] = df_ba.groupby(['month_year'])['death_by_date'].transform('mean')
df_ba_month = df_ba[['month_year', 'positive_by_month', 'death_by_month']].drop_duplicates()

def plot_ba(data, col1, col2, title, fname):
    fig, ax = plt.subplots(figsize=(15,7))
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Number of Cases', fontsize=14)
    ax.axvline(datetime(2020,5,16), color='k', linestyle='--')
    dstart = datetime(2020,4,1)
    dend = datetime(2020,11,30)
    ax.set_xlim([dstart, dend])
    ax = plt.scatter(data[col1].tolist(), data[col2], 
                 color='tab:orange', alpha=0.5, edgecolors='none')
    plt.savefig(fname)
    plt.show()

plot_ba(df_ba, 'date', 'new_case_by_date', 'Average Number of Daily Cases', 'dailycase_before_after.png')


