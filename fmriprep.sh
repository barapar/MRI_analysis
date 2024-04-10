# fMRIPrep code BASH
# input: a folder with sub-folders "sub-01" etc.
# replace "sub-01" with the sub label to preprocess
# --fs-license-file : free surfer licence, download separately

fmriprep-docker /home/lisz/Desktop/Time_project/time_fmri/data \
                /home/lisz/Desktop/Time_project/time_fmri/data/derivatives/preprocess \
                participant \
                --participant-label sub-01 \
                --fs-license-file /home/lisz/Desktop/Time_project/time_fmri/license.txt