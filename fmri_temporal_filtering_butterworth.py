'''
Butterworth filtering of the timescales
'''
import os
import numpy as np
import nibabel as nib
from os.path import join as opj
from nilearn.signal import butterworth

sub_list = ["sub-01","sub-02","sub-03",
            "sub-04","sub-05","sub-06",
            "sub-07","sub-08","sub-09",
            "sub-10","sub-11","sub-12",
            "sub-13","sub-15","sub-16",
            "sub-17","sub-18","sub-19",
            "sub-21","sub-22","sub-23",
            "sub-24","sub-25","sub-26",
            "sub-27","sub-28","sub-30",
            "sub-31","sub-32","sub-33",]

# root directory
root_dir = opj('/', 'home', 'lisz', 'Desktop')

# input directory
in_dir = opj(root_dir, 'Time_project', 'time_fmri', 'data', 'derivatives', 'preprocess')

# output directory and filename
out_name = f"{sub}_temporal_smoothing.nii.gz"
out_dir = opj(root_dir, 'Time_project', 'time_fmri', 'data', 'derivatives', 'autocorr_analysis_v2')

# open and load the atlas
atlas_dir = opj(root_dir, 'fmri_atlases', 'HCPex_2mm_resampled.nii.gz')
atlas_file = nib.load(atlas_dir)
atlas_img = atlas_file.get_fdata()

# create binary atlas
# since atlas has brain values from 1 to 426, take voxels unequal to 0
mask_atl = (atlas_img != 0)
atlas_img[mask_atl] = 1

###################################################################################
# matrix was taken from resting state data after
# regfilt transformation to isometric voxels
###################################################################################

affine_m = np.array([[   2.      ,    0.      ,    0.      ,  -95.97200775],
       [   0.      ,    2.      ,    0.      , -132.5     ],
       [   0.      ,    0.      ,    2.      ,  -78.5     ],
       [   0.      ,    0.      ,    0.      ,    1.      ]])

'''
open the file 
mask tha brain voxels
butterworth filtering
save to the nifti file for the next step
'''
for sub in sub_list:
    for root, dirs, files in os.walk(os.path.join(in_dir, sub, 'func')):
        for file in files:
            if file.endswith("_task-rest_acq-EPI_space-MNI152NLin2009cAsym_desc-preproc_bold_2mm-regfilt.nii.gz"):
                file_path = os.path.join(root, file)
                # load nifti
                img = nib.load(file_path)
                img_data = img.get_fdata()
                # mask the brain voxels
                img_data_masked = img_data[atlas_img == 1]
                # temporal filtering
                for idx, data in enumerate(img_data_masked):
                    f_tcs = butterworth(data, sampling_rate=0.5,
                                        high_pass=0.01, low_pass=0.1)
                    # return filtered data into the dataset
                    img_data_masked[idx] = f_tcs
                # save the array to the brain matrix and save
                # masked matrix should have the same shape as img_data
                masked_matrix = np.zeros((97, 116, 98, 180))
                masked_matrix[atlas_img == 1] = img_data_masked

                # use affine matrix from the RS file
                nifti_img = nib.Nifti1Image(masked_matrix, affine=affine_m)

                # Save the NIfTI image to file
                nib.save(nifti_img, out_dir + out_name)
                print(sub)