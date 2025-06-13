# Spike sorting quality control metrics

The quality metrics used in the IBL to determine good quality neurons are the following

* Sliding refractory period violation confidence level must be >90%
* Amplitude median must be > 50uV, 
* Noise cutoff metric < 5. 

See the [IBL's spike sorting whitepaper](https://figshare.com/articles/online_resource/Spike_sorting_pipeline_for_the_International_Brain_Laboratory/19705522?file=49783080) for an in-depth discussion of the single unit metrics.

In this section you will explore single units using the [IBL visualisation page]([Visualisation website](https://viz.internationalbrainlab.org/app?spikesorting=ss_2024-05-06&dset=bwm&pid=dab512bd-a02d-4c1f-8dbc-9155a163efc0&tid=0&cid=534&qc=1)) to get a feel for the QC metrics
