##
'''
Project 1
'''

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

LOCAL_PATH = Path('/Users/gaelle/Documents/Work/Course')

# Load the data
df_sess = pd.read_parquet(LOCAL_PATH.joinpath('sessions.pqt'))
df_subj = pd.read_parquet(LOCAL_PATH.joinpath('subjects.pqt'))
df_trial = pd.read_parquet(LOCAL_PATH.joinpath('trials.pqt'))

##
# Compute reaction time
df_trial['reaction_time'] = df_trial['response_times'] - df_trial['goCue_times']

# Merge
df_sess = df_sess.merge(df_subj[['subj_id', 'sex']], on='subj_id')
df_trial = df_trial.merge(df_sess[['eid', 'sex', 'subject']], on='eid')  # Added in subject for boxplot

# Keep only trials where it was a choice
df_trial_ch = df_trial.loc[(df_trial['choice'] != 0) & (df_trial['reaction_time'] > 0)]
##
'''
Compare the reaction times on the first and last N trials:

Define N: for this, you will need to first find the minimum session length (in terms of trial number), 
and use 1/3 of this value as N. For example, 
if the minimum session length is 300, you will set N as int(300/3) = 100 (we use integers).
Across all sessions, select the first and last N trials.
Using the K-S test, assess whether the reaction time distributions (across all mice) 
are different for first versus last trials.
Plot the two distributions using boxplot.
Are the reaction times significantly different for first and last trials?
'''
# Find min session length, and compute N accordingly
min_n_trial = min(df_trial_ch.groupby('eid').size())
n_trial = int(min_n_trial/3)

# Get first and last N trials
df_first = df_trial_ch.groupby('eid').head(n_trial)
df_last = df_trial_ch.groupby('eid').tail(n_trial)

# Note: if you want to take arbitrary rows, here from 23:69:
df_arbit = df_trial_ch.groupby('eid').apply(lambda x: x[23:69])

# KS-test
results_ks = ks_2samp(df_first['reaction_time'], df_last['reaction_time'])
print(results_ks)

# Plot
# Merge the df
df_first['trial_type'] = 'first'
df_last['trial_type'] = 'last'
df_merge = pd.concat([df_first, df_last])

# Create 2 subplots with linear and log y-axis
fig = plt.figure(figsize=(9, 3))
ax = plt.subplot(1, 2, 1)
df_merge.plot.box(column="reaction_time", by="trial_type", ax=ax)
ax.set_yscale('linear')

ax = plt.subplot(1, 2, 2)
df_merge.plot.box(column="reaction_time", by="trial_type", ax=ax)
ax.set_yscale('log')
##
'''
Compare male and female mice:

Group the data by male and female mice.
Using the K-S test, assess whether the session length (i.e. number of trial) distributions are different for 
male versus female mice
Plot the distributions using histogram
Do you think that male mice do longer sessions than female mice?
Using the K-S test, assess whether the reaction time distributions in late trials (only) are different for 
male versus female mice
Plot the distributions using KDE
Do female mice respond differently than male mice in late trials?
'''

df_n_trial = df_trial_ch.groupby('eid', as_index=False).size()  # The size is the N trial
# Merge to get sex information
df_n_trial = df_n_trial.merge(df_trial_ch[['eid', 'sex']], on='eid')
df_n_trial = df_n_trial.drop_duplicates()  # Remove all duplicates row per trials

ks_2samp(df_n_trial.groupby('sex').get_group('M')['size'],
         df_n_trial.groupby('sex').get_group('F')['size'])

# Plot the KDE for both male and female mice
df_n_trial.groupby('sex')['size'].plot(kind='kde')

# Add legends for the curves (sex)
plt.legend(df_trial.groupby('sex').sex.dtype.index.to_list(), title='Sex')
