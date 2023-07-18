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
df_trial = df_trial.merge(df_sess[['eid', 'sex']], on='eid')

# Count how many trials for M / F mice
tr_fm = df_trial.groupby('sex')['reaction_time'].count()
print(tr_fm)
# Proportion of Female over Male mice
pr_fm = tr_fm['F'] / tr_fm['M']
