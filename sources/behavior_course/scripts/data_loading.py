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
    # Get date
    df_sess['date'] = df_sess['start_time'][0][0:10]
    # Remove some columns
    df_sess = df_sess.drop(columns=['projects', 'url', 'number', 'start_time'])

    # Hit database to get subject information
    subj = one.alyx.rest('subjects', 'list', nickname=sess[0]['subject'])
    df_subj = pd.DataFrame.from_dict(subj)
    # Keep only some info
    keys_keep = ['nickname', 'id', 'birth_date', 'sex']
    # Drop columns
    df_subj = df_subj[df_subj.columns[df_subj.columns.isin(keys_keep)]]
    # Rename column id to subj_id
    df_subj = df_subj.rename(columns={"id": "subj_id"})

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

# Save dataframes
df_sess_all.to_csv(LOCAL_PATH.joinpath('sessions.csv'))
df_subj_all.to_csv(LOCAL_PATH.joinpath('subjects.csv'))
df_trial_all.to_csv(LOCAL_PATH.joinpath('trials.csv'))

##
#
# subject = 'SWC_043'
# trials = one.load_aggregate('subjects', subject, '_ibl_subjectTrials.table')
#
# # Load training status and join to trials table
# training = one.load_aggregate('subjects', subject, '_ibl_subjectTraining.table')
# trials = (trials
#           .set_index('session')
#           .join(training.set_index('session'))
#           .sort_values(by=['session_start_time', 'intervals_0']))
# trials['training_status'] = trials.training_status.fillna(method='ffill')
#
# ##
# from pathlib import Path
# import dask.dataframe as dd
# path_sess = Path('/Users/gaelle/Documents/Work/Course').joinpath('all_action_kernel_sessions.pqt')
# path_trial = Path('/Users/gaelle/Documents/Work/Course').joinpath('all_blocked_trials.pqt')
#
# df_sess = dd.read_parquet(path_sess).compute()
# df_trial = dd.read_parquet(path_trial).compute()
