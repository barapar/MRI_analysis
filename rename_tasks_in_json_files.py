'''
add task name to json files
'''
import os

# the path to the input data folder
data_dir = '/home/lisz/Desktop/Time_project/time_fmri/data/derivatives/preprocess'

# List of participants to process
sub_list = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09",
            "sub-10","sub-11","sub-12", "sub-13","sub-15","sub-16", "sub-17","sub-18","sub-19",
            "sub-21","sub-22","sub-23", "sub-24","sub-25","sub-26", "sub-27","sub-28","sub-30",
            "sub-31","sub-32","sub-33"]

def rename_task(subfolder):

    if subfolder == 'func':
        listdirectory = os.listdir(".")  # gets the name of all files in your dir
