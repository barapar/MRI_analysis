'''
rename NIFTI files to BIDS format
'''

import os
import shutil
from os.path import join as opj

# input the subject label
# sub-01 
sub = input('Plese enter subject number: ') 

# root directory
root_dir = opj('/', 'home', 'lisz', 'Desktop', 'Time_project', 'time_fmri', 'data')

# directory with files to-be-renamed
nifti_dir = opj(root_dir, sub) 
anat_dir = opj(nifti_dir, 'anat') # folder to save anatomical data
func_dir = opj(nifti_dir, 'func') # folder to save functional data

# the endings of the files to be renamed, 'a' corresponds to second run, 'b' to the third run etc
list_json = ['4.json', '4a.json', '4b.json', '4c.json']
list_nifti = ['4.nii.gz', '4a.nii.gz', '4b.nii.gz', '4c.nii.gz']
runs = ['1','2','3','4']

# for functional data: rename the file and move to another folder
def epi_rename_and_move(nifti_dir, name_ending, new_folder,ext,run):
    for filename in os.listdir(nifti_dir):
        if filename.endswith(name_ending):
            old_file_path = os.path.join(nifti_dir, filename)
            new_filename = filename.replace(sub+'_EPI_TR2000_TE25_205_F1-'+name_ending, sub+'_task-reproduction_run-0'+run+ext)
            new_file_path = os.path.join(new_folder, new_filename)
            shutil.move(old_file_path, new_file_path)

for name_ending, run in zip(list_json, runs):
	epi_rename_and_move(nifti_dir, name_ending, func_dir,'_bold.json',run)
for name_ending, run in zip(list_nifti, runs):
	epi_rename_and_move(nifti_dir, name_ending, func_dir,'_bold.nii.gz',run)

# for resting state: rename the file and move to another folder
def rest_rename_and_move(nifti_dir, name_ending, new_folder,ext):
    for filename in os.listdir(nifti_dir):
        if filename.endswith(name_ending):
            old_file_path = os.path.join(nifti_dir, filename)
            new_filename = filename.replace(sub+'_Resting_State_TR2000_M180_OPEN_'+name_ending, sub+'_task-rest_acq-EPI_bold'+ext)
            new_file_path = os.path.join(new_folder, new_filename)
            shutil.move(old_file_path, new_file_path)

rest_rename_and_move(nifti_dir, 'EYE.json', func_dir,'.json')
rest_rename_and_move(nifti_dir, 'EYE.nii.gz', func_dir,'.nii.gz')

# for anatomical data: rename the file and move to another folder
def anat_rename_and_move(nifti_dir, name_ending, new_folder,ext):
    for filename in os.listdir(nifti_dir):
        if filename.endswith(name_ending):
            old_file_path = os.path.join(nifti_dir, filename)
            new_filename = filename.replace(sub+'_MPRAGE_Sag_1mm_iso_'+name_ending, sub+'_T1w'+ext)
            new_file_path = os.path.join(new_folder, new_filename)
            shutil.move(old_file_path, new_file_path)

anat_rename_and_move(nifti_dir, 'g2.json', anat_dir,'.json')
anat_rename_and_move(nifti_dir, 'g2.nii.gz', anat_dir,'.nii.gz')
