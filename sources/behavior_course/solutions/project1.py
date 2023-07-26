##
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
df_trial['reaction_time_trig'] = df_trial['response_times'] - df_trial['goCueTrigger_times']
df_trial['reaction_time'] = df_trial['response_times'] - df_trial['goCue_times']
df_trial['reaction_time_diff'] = df_trial['reaction_time'] - df_trial['reaction_time_trig']

# Merge
df_sess = df_sess.merge(df_subj[['subject', 'sex']], on='subject')
df_trial = df_trial.merge(df_sess[['eid', 'sex', 'subject']], on='eid')  # Added in subject for boxplot

##
# Questions in text

# Count how many trials for M / F mice
tr_fm = df_trial.groupby('sex')['reaction_time'].count()
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