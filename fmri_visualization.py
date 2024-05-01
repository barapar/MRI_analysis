'''
Visualization of the BOLD signal on th brain surface
'''
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib as mpl
from nilearn import surface
from nilearn import plotting
from nilearn import datasets
from os.path import join as opj

# project directory
root_dir = opj('/', 'home', 'lisz', 'Desktop', 'Time_project', 'time_fmri', 'data',
                        'derivatives', 'glm_complex_anova', 'glm_group_level')

# end of the filename to visualise
img_name = '/cope1.feat/thresh_zstat1.nii.gz'

contrast = '/contrast1.gfeat'

# download a Freesurfer fsaverage surface
fsaverage = datasets.fetch_surf_fsaverage()

##############################################################################################
# load image
img = nib.load(root_dir + contrast + img_name)

# load atlas
destrieux_atlas = datasets.fetch_atlas_surf_destrieux()
# choose hemisphere
parcellation = destrieux_atlas['map_right']

# regions to outline on the brain surface
regions_dict = {b'G_postcentral': 'Postcentral gyrus',
                b'G_precentral': 'Precentral gyrus'}

# get indices in atlas for these labels
regions_indices = [
    np.where(np.array(destrieux_atlas['labels']) == region)[0][0]
    for region in regions_dict]

# set labels
labels = list(regions_dict.values())

# load img data
texture = surface.vol_to_surf(img, fsaverage.pial_left)

# choose colormap
cmap = mpl.cm.plasma # pink - yellow

#####################################################################################
# plot surface (simple, one hemisphere)
#####################################################################################
fig = plotting.plot_surf_stat_map(
    fsaverage.infl_left, texture,
    hemi='left',
    threshold=3.1,
    bg_map=fsaverage.sulc_left,
    view='lateral',
    vmax=8.3,
    bg_on_data=True)

plotting.plot_surf_contours(fsaverage.infl_right, parcellation, labels=labels,
                            levels=regions_indices, figure=fig,
                            legend=True,
                            colors=['g', 'k'])
fig.show()

#####################################################################################
# plot surface (two hemispheres, both views)
#####################################################################################
plotting.plot_img_on_surf(img, bg_on_data = True,
                          views=['medial', 'lateral'],
                          hemispheres=['left', 'right'],
                          colorbar=True,
                          cmap = 'seismic',
                          inflate=True,
                          threshold=3.1)
plotting.show()

#####################################################################################
# plot slices based on activation (or set manually)
#####################################################################################
plotting.plot_stat_map(img, threshold=3.1,
                       # choose particular slices
                       cut_coords=(-30,-5,1,10,17),
                       # of choose amount of slices
                       #cut_coords=5,
                       draw_cross=False,
                       display_mode="z",
                       #vmax=1,upperbond of the colormap
                       colorbar=True,
                       title="First event")
plt.savefig(pth+"first_event.png", dpi=1000)