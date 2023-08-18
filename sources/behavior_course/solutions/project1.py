##
'''
Project 1

Using the df_trial_ch dataframe:

Compare the reaction times on the first and last N trials:

Define N: for this, you will need to first find the minimum session length (in terms of trial number), and use 1/3 of this value as N. For example, if the minimum session length is 300, you will set N as int(300/3) = 100 (we use integers).
Across all sessions, select the first and last N trials.
Using the K-S test, assess whether the reaction time distributions (across all mice) are different for first versus last trials.
Plot the two distributions using boxplot.
Are the reaction times significantly different for first and last trials?
Compare male and female mice:

Group the data by male and female mice.
Using the K-S test, assess whether the session length (i.e. number of trial) distributions are different for male versus female mice
Plot the distributions using histogram
Do you think that male mice do longer sessions than female mice?
Using the K-S test, assess whether the reaction time distributions in late trials (only) are different for male versus female mice
Plot the distributions using KDE
Do female mice respond differently than male mice in late trials?
'''

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

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
'''
# Find min session length, and compute N accordingly
min_n_trial = min(df_trial_ch.groupby('eid').size())
n_trial = int(min_n_trial/3)

# Get first and last N trials
df_first = df_trial_ch.groupby('eid').head(n_trial)
df_last = df_trial_ch.groupby('eid').tail(n_trial)



##
# Questions in text

# Count how many trials for M / F mice
tr_fm = min(df_trial.groupby('sex')['reaction_time'].size())
print(tr_fm)
# Proportion of Female over Male mice
pr_fm = tr_fm['F'] / tr_fm['M']

# Get negative RTs
df_trial_neg_rt = df_trial[df_trial['reaction_time'] < 0]

# Plot the distribution of trial number for negative reaction time per subject
df_trial_neg_rt.plot.box(column="trial_number", by="subject")
# Count how many trials for each subject
tr_sub = df_trial_neg_rt.groupby('subject')['reaction_time'].count()
print(tr_sub)
# outlier subject: KS023

##
# Further questions

# Get positive RTs
df_trial_pos_rt = df_trial[df_trial['reaction_time'] > 0]

# Plot the distribution of reaction time for male and female mice using `hist`, and `boxplot`
# Histogram
df_trial_pos_rt.groupby('sex')['reaction_time'].plot(kind='kde')
# Add legends for the curves (sex)
plt.legend(df_trial_pos_rt.groupby('sex').sex.dtype.index.to_list(), title='Sex')
# Box plot
df_trial_pos_rt.plot.box(column="reaction_time", by="sex")

# Plot the distribution of reaction time per subject using `boxplot`
df_trial_pos_rt.plot.box(column="reaction_time", by="subject")
