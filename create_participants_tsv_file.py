'''
to run fMRIPrep, create participants.tsv
it contains on column named 'participant_id'
one row = one int
ex.: for "sub-01" write 1
'''
# the path to the output data folder
out_dir = '/home/lisz/Desktop/Time_project/time_fmri/data'

participants_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                     11, 12, 13, 15, 16, 17, 18, 19,
                     21, 22, 23, 24, 25, 26, 27, 28,
                     30, 31, 32, 33]

# open the file, if it does not exist it will be created
with open(out_dir + '/participants.tsv', 'w') as f:
    # write the column name and move to the next row with \n
    f.write('participant_id\n')
    # write each participant number on a new row
    for participant in participants_list:
        f.write(f'{participant}\n')
