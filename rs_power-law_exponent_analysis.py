'''
Calculate the power law exponent for resting state data
with further corellation of the exponent to behaviral data with permutation test
input: temporally and spatially smoothed data
Parallel jobs are implemented to increase the speed of computations
'''
import os
from nitime.timeseries import TimeSeries
from nitime.analysis import SpectralAnalyzer
import nibabel as ni
import numpy as np
import pandas as pd
import nipype.interfaces.fsl as fsl
from joblib import Parallel, delayed
from scipy.optimize import curve_fit
from numpy import mean,std,zeros

# repetition time of the rs data
tr=2
# how many jobs in parallel is planned to run
cores=8
# amplitude range
rng=(0.01,0.1)
# full width half maximum - for the naming of the temporally smoothed data
fwhm = 6

# global directory
data_dir = os.path.join('/', 'home', 'lisz', 'Desktop', 'Time_project', 'time_fmri', 'data', 'derivatives')

# folder with the input data
preproc_dir = os.path.join(data_dir, 'autocorr_analysis_v2')

# output directory
output_dir = os.path.join(data_dir, 'power-low_analysis')

# directory of the behavioral data
behav_dir = os.path.join('/', 'home', 'lisz', 'Desktop', 'Time_project', 'time_fmri', 'behavioral_data')
behav_dir = "/home/lisz/Desktop/Time_project/time_fmri/behavioral_data"

# List of participants to process
sub_list = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09",
            "sub-10", "sub-11", "sub-12", "sub-13", "sub-15", "sub-16", "sub-17", "sub-18", "sub-19",
            "sub-21", "sub-22", "sub-23", "sub-24", "sub-25", "sub-26", "sub-27", "sub-28", "sub-30",
            "sub-31", "sub-32", "sub-33",]

mask_img = ni.load(os.path.join(data_dir, 'autocorr_analysis_v2', 'grey_mask.nii.gz'))
mask_data = mask_img.get_fdata()
affine = mask_img.affine


### Shared functions
def get_img_data(imgP):
    #img=ni.get_fdata(imgP)
    img=ni.load(imgP)
    aff=img.affine
    img=img.get_fdata()
    return img,aff

def find_nearest(array,value):
  idx=(abs(array-value)).argmin()
  return idx

def fitting_func(x,a,b):
    return a*(1/x**b)

def calc_tcs_ple(tcs,i):
    T=TimeSeries(tcs[i],sampling_interval=tr)
    S=SpectralAnalyzer(T)
    p=S.spectrum_multi_taper[1]
    popt,pcov=curve_fit(fitting_func,freq[a:b],p[a:b])
    return(popt[1])

def make_beta_img(imgP,roiP,outP):
    img,aff=get_img_data(imgP)
    roi=get_img_data(roiP)[0]
    tcs=img[roi==1]
    tcs=(tcs-mean(tcs,axis=1,keepdims=True))/std(tcs,axis=1,keepdims=True)
    T=TimeSeries(tcs[0,:],sampling_interval=tr)
    S=SpectralAnalyzer(T)
    freq,psd=S.spectrum_multi_taper
    a=find_nearest(freq,rng[0])
    b=find_nearest(freq,rng[1])
    tcs[:] = np.nan_to_num(tcs, nan=0.0)
    beta=Parallel(n_jobs=cores)(delayed(calc_tcs_ple)(tcs,i)for i in range(tcs.shape[0]))
    out=zeros(img.shape[0:3])
    out[roi==1]=beta
    out=ni.Nifti1Image(out,aff)
    out_file = os.path.join(outP, f'{subject}powerlaw_exponents.nii.gz')
    out.to_filename(out_file)
    print(f"{subject} done")


#imgP=os.path.join()
roiP=os.path.join(preproc_dir, 'grey_mask.nii.gz')
outP=output_dir


# calculate this function for each subject
# and then check the output and create a shared image
# since putput is also going to be just 1 value
for subject in sub_list:
    imgP = os.path.join(preproc_dir, f"{subject}_temporal_smoothing.nii.gz")
    make_beta_img(imgP, roiP, outP)

################################################################################

if not os.path.isdir(os.path.join(output_dir, 'randomise_behav_corr')):
    os.mkdir(os.path.join(output_dir, 'randomise_behav_corr'))

if not os.path.isdir(os.path.join(output_dir, 'randomise_abs_behav_corr')):
    os.mkdir(os.path.join(output_dir, 'randomise_abs_behav_corr'))

### Make group image
grp_img = np.zeros(np.hstack((mask_data.shape, len(sub_list))))
for ss, subject in enumerate(sub_list):
    fname = os.path.join(output_dir, f'{subject}powerlaw_exponents.nii.gz')
    grp_img[:, :, :, ss] = ni.load(fname).get_fdata()

# save group image
out_img = ni.Nifti1Image(grp_img, affine=affine)
out_img.to_filename(os.path.join(output_dir, "group_voxel_PLE.nii.gz"))

#######################################################################################
### Permutation test
#######################################################################################

# depending on research question, which folder is in work now?
analysis_folder = 'randomise_abs_behav_corr'

# Design file with subject mean RTs
with open(os.path.join(output_dir, analysis_folder, 'design.mat'), 'w') as fname:
    fname.write('/NumWaves\t2\n')
    fname.write(f'/NumPoints\t{len(sub_list)}\n')
    fname.write('/PPheights\t1\n')
    fname.write('\n/Matrix\n')
    for subject in sub_list:
        df = pd.read_csv(os.path.join(behav_dir, subject, f'{subject}_all_runs.csv'), index_col=0)
        df = df.iloc[1:, :]
        df = df.loc[df['exclusion'] != 'exclude']
        if analysis_folder == 'randomise_abs_behav_corr':
            fname.write(f"1\t{np.abs(np.mean(df['key_resp_rt'])-2)}\n")
        else:
            fname.write(f"1\t{np.abs(np.mean(df['key_resp_rt']))}\n")

# Contrast file
with open(os.path.join(output_dir, analysis_folder, 'design.con'), 'w') as fname:
    fname.write('/ContrastName1\tMean RT\n')
    fname.write('/NumWaves\t2\n')
    fname.write('/NumContrasts\t2\n')
    fname.write('/PPheights\t1\n')
    fname.write('/RequiredEffect\t1\n')
    fname.write('\n/Matrix\n')
    fname.write('0\t1\n')
    fname.write('0\t-1\n')

### Run randomise
rand = fsl.Randomise(in_file=os.path.join(output_dir, 'group_voxel_PLE.nii.gz'),
                     mask=os.path.join(data_dir, 'autocorr_analysis_v2', 'grey_mask.nii.gz'),
                     tcon=os.path.join(output_dir, analysis_folder, 'design.con'),
                     design_mat=os.path.join(output_dir, analysis_folder, 'design.mat'),
                     base_name=os.path.join(output_dir, analysis_folder, 'behav_corr'),
                     raw_stats_imgs=True,
                     tfce=True,
                     vox_p_values=True,
                     num_perm=5000)


rand.run()