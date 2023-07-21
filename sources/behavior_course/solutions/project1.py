##
import pandas as pd
from pathlib import Path

LOCAL_PATH = Path('/Users/gaelle/Documents/Work/Course')

# Load the data
df_sess = pd.read_parquet(LOCAL_PATH.joinpath('sessions.pqt'))
df_subj = pd.read_parquet(LOCAL_PATH.joinpath('subjects.pqt'))
df_trial = pd.read_parquet(LOCAL_PATH.joinpath('trials.pqt'))

##
# Compute reaction time
df_trial['reaction_time'] = df_trial['response_times'] - df_trial['goCue_times']

# Merge
df_sess = df_sess.merge(df_subj[['subject', 'sex']], on='subject')
df_trial = df_trial.merge(df_sess[['eid', 'sex', 'subject']], on='eid')  # Added in subject for boxplot

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
