##
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

    return df_sess, df_subj, df_trials


# eid = sessions_bw[0]
for index, eid in enumerate(sessions_bw):
    df_sess, df_subj, df_trial = get_trial_sess_subj_df(eid, one)
    if index == 0:  # Create first df from scratch
        df_sess_all = df_sess.__deepcopy__()
        df_subj_all = df_subj.__deepcopy__()
        df_trial_all = df_trial.__deepcopy__()
        continue
    # Concatenate subsequent df
    df_sess_all = pd.concat([df_sess_all, df_sess])
    df_subj_all = pd.concat([df_subj_all, df_subj])
    df_trial_all = pd.concat([df_trial_all, df_trial])

# Remove duplicates in subjects table
df_subj_all = df_subj_all.drop_duplicates(subset=["subj_id"], keep='first')

# Sort
df_sess_all = df_sess_all.sort_values(by=['subject', 'date_time'])
df_subj_all = df_subj_all.sort_values(by=['subject'])

# Save dataframes
df_sess_all.to_parquet(LOCAL_PATH.joinpath('sessions.pqt'), index=False)  # index=False to get rid of Unnamed column
df_subj_all.to_parquet(LOCAL_PATH.joinpath('subjects.pqt'), index=False)
df_trial_all.to_parquet(LOCAL_PATH.joinpath('trials.pqt'), index=False)

