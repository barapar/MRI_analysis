#!/bin/bash
# image resampling

INPUT_DIR='/home/lisz/Desktop/Time_project/time_fmri/data/derivatives/preprocess/${SUBJECT_ID}/func'

# Path to the participants.tsv file generated by fmriprep
TSV_FILE='/home/lisz/Desktop/Time_project/time_fmri/data/participants.tsv'

# Extract subject IDs from the participants.tsv file
SUBJECT_IDS=($(awk -F '\t' 'NR>1 {print "sub-"$1}' "${TSV_FILE}"))

# List of subject IDs
SUBJECT_IDS=('sub-33' 'sub-34' 'sub-35')  # Add more subjects as needed

# Loop over subjects
for SUBJECT_ID in "${SUBJECT_IDS[@]}"; do
    # Set the input and output paths for the functional image
    INPUT_IMAGE="${INPUT_DIR}/${SUBJECT_ID}_task-rest_acq-EPI_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    OUTPUT_IMAGE="${INPUT_DIR}/${SUBJECT_ID}_task-rest_acq-EPI_space-MNI152NLin2009cAsym_desc-preproc_bold_2mm.nii.gz"

    # Print information about the current subject being processed
    echo "Processing subject: ${SUBJECT_ID}"

    # Run the FLIRT command
    flirt -in "${INPUT_IMAGE}" \
          -ref "${INPUT_IMAGE}" \
          -applyisoxfm 2 \
          -out "${OUTPUT_IMAGE}"

    # Print a separator for better readability
    echo "----------------------------------------"

done