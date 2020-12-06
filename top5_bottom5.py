import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns 
sns.set_style('darkgrid')


#load the merged dataset
os.getcwd()
path_with_os = os.path.expanduser(r'~\Documents\GitHub\Nadia-and-Yuwen-final-project')
file = os.path.join(path_with_os, 'data.csv')
df = pd.read_csv(file, header=0)
df.dtypes



# get data before Nov.30
df = df[df['date'] <= '2020-11-30']

#change to datetime format
df['date'] = pd.to_datetime(df['date'])
df['policy_date'] = pd.to_datetime(df['policy_date'])
df.dtypes

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
    #plt.show()
    

    png_path = os.path.join(path_with_os, '{}.png'.format(which_states[5]))
    plt.savefig(png_path, bbox_inches='tight') #add "bbox_inches='tight'" to avoid cutoff title
    print('Image saved: ', png_path)
    plt.close()

#draw graph for 5 states with the highest average daily new cases
plot_together(top_5)
#draw graph for 5 states with the lowest average daily new cases
plot_together(low_5)
