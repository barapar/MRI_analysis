#!/bin/bash
"""
spatial smoothing with fslmaths, FWHM method
"""

output_directory="/home/lisz/Desktop/Time_project/time_fmri/data/derivatives/autocorr_analysis_v2/"


sub_list=("sub-01" "sub-02" "sub-03"
            "sub-04" "sub-05" "sub-06"
            "sub-07" "sub-08" "sub-09"
            "sub-10" "sub-11" "sub-12"
            "sub-13" "sub-15" "sub-16"
            "sub-17" "sub-18" "sub-19"
            "sub-21" "sub-22" "sub-23"
            "sub-24" "sub-25" "sub-26"
            "sub-27" "sub-28" "sub-30"
            "sub-31" "sub-32" "sub-33")

# Define the FWHM values in millimeters
fwhm=6

# Calculate the smoothing sigma corresponding to the FWHM value
# https://kathleenhupfeld.com/how-to-smooth-images-in-fsl-its-different-from-spm/
# bc -l - tells the function to use the standard math library
# scale=3 - 3 decimal places in the result
sigma=$(echo "scale=3; $fwhm / 2.354" | bc -l)

# Loop over each FWHM value
for sub in "${sub_list[@]}"; do

    input_image="${output_directory}/${sub}_temporal_smoothing.nii.gz"

    output_image="${output_directory}/${sub}_spatially_smoothed_${fwhm}mm.nii.gz"

    # spatial smoothing using fslmaths
    fslmaths "$input_image" -s "$sigma" "$output_image"

    echo "Smoothed ${fwhm}mm: ${output_image}"
done