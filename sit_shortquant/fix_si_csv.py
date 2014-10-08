# fix_si_csv.py
# by Ryan Delgado 10/5/2014
# The purpose of this script is to fix csv files containing short interest data in the TuFeb192013 directory.
# The csv files in this directory have no column names. This script will read in the csv files, insert column names,
# and then reprint the csv files.

import pandas as pd
import os


si_dir = '/home/ryan/Desktop/sit_shortquant/short_interest/TueFeb192013'
file_names = os.listdir(si_dir)
column_names = ['filename','ticker_in_file','Settlement Date', 'Short Interest', 'Avg Daily Share Volume',
                'Days To Cover']

def read_file(directory, file_name):
    if os.stat('%s/%s' % (directory, file_name)).st_size == 0:
        return pd.DataFrame()
    si_file = open('%s/%s' % (directory, file_name), 'r')
    lines = []
    for line in si_file:
        row = line.split(' ')
        row = [entry.replace('\n', '') for entry in row]
        row2 = []
        for entry in row:
            if entry is not '':
                row2.append(entry)

        lines.append(row2)

    return pd.DataFrame(lines)

for file_name in file_names:
    if '^' in file_name:
        os.remove('%s/%s' % (si_dir, file_name))
    else:
        frame = read_file(si_dir, file_name)
        print 'Reading in', file_name, '...'

        if (frame.shape[1] == 0) or (frame.shape[1] == 1) or (frame.shape[0] < 4):
            new_frame = pd.DataFrame()
        else:
            ticker = file_name[:len(file_name)-4]
            ticker_list = [ticker for x in range(24)]
            ticker_in_file = [ticker_list, ticker_list]
            ticker_frame = pd.DataFrame(ticker_in_file).transpose()
            pieces = [ticker_frame.ix[:,0], ticker_frame.ix[:,1], frame.ix[:,0], frame.ix[:,1], frame.ix[:,2], frame.ix[:,3]]
            new_frame = pd.concat(pieces, axis=1)
            new_frame.columns = column_names
            os.remove('%s/%s' % (si_dir, file_name))
            new_frame.to_csv('%s/%s' % (si_dir, file_name), index=False)