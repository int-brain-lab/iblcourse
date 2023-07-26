##
import numpy as np
import pandas as pd
from one.api import ONE
from pathlib import Path

one = ONE(base_url='https://openalyx.internationalbrainlab.org')
tag = '2022_Q4_IBL_et_al_BWM'
one.load_cache(tag=tag)
sessions_bw = one.search()  # All sessions used in the paper

LOCAL_PATH = Path('/Users/gaelle/Documents/Work/Course')

##
# To return to the full cache containing an index of all IBL experiments
ONE.cache_clear()
one = ONE(base_url='https://openalyx.internationalbrainlab.org')

##
# We create 3 tables: trials, subjects and sessions


def get_trial_sess_subj_df(eid, one):
    trials = one.load_object(eid, 'trials', collection='alf')
    df_trials = trials.to_df()
    df_trials['eid'] = eid
    # The index in the dataframe will be the trial number, but we put it here for simplicity
    df_trials['trial_number'] = np.arange(0, df_trials.shape[0])

    # Hit database to get session information
    sess = one.alyx.rest('sessions', 'list', id=eid)
    df_sess = pd.DataFrame.from_dict(sess)
    # Rename column id to eid
    df_sess = df_sess.rename(columns={"id": "eid"})
    # Get date and time
    df_sess['date_time'] = pd.to_datetime(df_sess['start_time'])  # access date with .dt.date
    # Remove some columns
    df_sess = df_sess.drop(columns=['projects', 'url', 'number', 'start_time'])

    # Hit database to get subject information
    subj = one.alyx.rest('subjects', 'list', nickname=sess[0]['subject'], lab=sess[0]['lab'])
    df_subj = pd.DataFrame.from_dict(subj)
    # Keep only some info
    keys_keep = ['lab', 'nickname', 'id', 'birth_date', 'sex']
    # Drop columns
    df_subj = df_subj[df_subj.columns[df_subj.columns.isin(keys_keep)]]
    # Rename column id to subj_id
    df_subj = df_subj.rename(columns={"id": "subj_id"})
    df_subj = df_subj.rename(columns={"nickname": "subject"})
    # Add in subj id to df_sess for merging later
    df_sess['subj_id'] = df_subj['subj_id']

    return df_sess, df_subj, df_trials


# eid = sessions_bw[0]
list_sess_all = list()
list_subj_all = list()
list_trial_all = list()

for index, eid in enumerate(sessions_bw):
    df_sess, df_subj, df_trial = get_trial_sess_subj_df(eid, one)
    # Append in list, then do aggregate outside the loop for df
    list_sess_all.append(df_sess)
    list_subj_all.append(df_subj)
    list_trial_all.append(df_trial)

df_sess_all = pd.concat(list_sess_all)
df_subj_all = pd.concat(list_subj_all)
df_trial_all = pd.concat(list_trial_all)

# df = pd.concat(list_of_dataframes)

# Remove duplicates in subjects table
df_subj_all = df_subj_all.drop_duplicates(subset=["subj_id"], keep='first')

# Sort
df_sess_all = df_sess_all.sort_values(by=['subject', 'date_time'])
df_subj_all = df_subj_all.sort_values(by=['subject'])

# Save dataframes
df_sess_all.to_parquet(LOCAL_PATH.joinpath('sessions.pqt'), index=False)  # index=False to get rid of Unnamed column
df_subj_all.to_parquet(LOCAL_PATH.joinpath('subjects.pqt'), index=False)
df_trial_all.to_parquet(LOCAL_PATH.joinpath('trials.pqt'), index=False)
