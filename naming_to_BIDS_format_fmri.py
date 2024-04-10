"""rename row MRI data  to BIDS"""

import os
import shutil

sub = input("Plese enter subject number: ") # sub-05 

pth = "/home/lisz/Desktop/Time_project/time_fmri/data"

base_folder = pth+"/"+sub # where are the files to be renamed
anat_fold = pth+"/"+sub+"/anat" # folder to save anatomical data
func_fold = pth+"/"+sub+"/func" # folder to save functional data

# the endings of the files, "a" corresponds to second run, "b" to third trial
list_json = ["4.json", "4a.json", "4b.json", "4c.json"]
list_nifti = ["4.nii.gz", "4a.nii.gz", "4b.nii.gz", "4c.nii.gz"]
runs = ["1","2","3","4"]

# for functional data: rename the file and move to another folder
def epi_rename_and_move(base_folder, ends, new_folder,ext,run):
    for filename in os.listdir(base_folder):
        if filename.endswith(ends):
            old_file_path = os.path.join(base_folder, filename)
            new_filename = filename.replace(sub+'_EPI_TR2000_TE25_205_F1-'+ends, sub+'_task-reproduction_run-0'+run+ext)
            new_file_path = os.path.join(new_folder, new_filename)
            shutil.move(old_file_path, new_file_path)

for ends, run in zip(list_json, runs):
	epi_rename_and_move(base_folder, ends, func_fold,"_bold.json",run)
for ends, run in zip(list_nifti, runs):
	epi_rename_and_move(base_folder, ends, func_fold,"_bold.nii.gz",run)

# for resting state: rename the file and move to another folder
def rest_rename_and_move(base_folder, ends, new_folder,ext):
    for filename in os.listdir(base_folder):
        if filename.endswith(ends):
            old_file_path = os.path.join(base_folder, filename)
            new_filename = filename.replace(sub+'_Resting_State_TR2000_M180_OPEN_'+ends, sub+'_task-rest_acq-EPI_bold'+ext)
            new_file_path = os.path.join(new_folder, new_filename)
            shutil.move(old_file_path, new_file_path)

rest_rename_and_move(base_folder, 'EYE.json', func_fold,".json")
rest_rename_and_move(base_folder, 'EYE.nii.gz', func_fold,".nii.gz")

# for anatomical data: rename the file and move to another folder
def anat_rename_and_move(base_folder, ends, new_folder,ext):
    for filename in os.listdir(base_folder):
        if filename.endswith(ends):
            old_file_path = os.path.join(base_folder, filename)
            new_filename = filename.replace(sub+'_MPRAGE_Sag_1mm_iso_'+ends, sub+'_T1w'+ext)
            new_file_path = os.path.join(new_folder, new_filename)
            shutil.move(old_file_path, new_file_path)

anat_rename_and_move(base_folder, 'g2.json', anat_fold,".json")
anat_rename_and_move(base_folder, 'g2.nii.gz', anat_fold,".nii.gz")
