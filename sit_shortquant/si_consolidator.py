# si_consolidator.py
# by Ryan Delgado 10/4/2014
# The purpose of this script is to consolidate all of the short interest data
# in a given directory into csv files for each stock.

import pandas as pd
import os
import fnmatch
import sys



def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                path = os.path.join(root)
                yield path



def read_si_file(directory, file_name):
    if os.stat('%s/%s' % (directory, file_name)).st_size == 0:  # somme csv files are just empty
        return pd.DataFrame()
    else :
        frame = pd.read_csv('%s/%s' % (directory, file_name), header=0, index_col=2)
        frame = pd.DataFrame(frame['Short Interest'])  # focus only on the short interest data
        ticker = file_name[:len(file_name)-4]  # ticker name of file
        frame.columns = [ticker]
        frame.index = pd.to_datetime(frame.index)
        return frame



def main(argv):
    root_dir = argv[1]
    print root_dir
    si_store_dir = argv[2]
    print si_store_dir
    si_store = pd.HDFStore(si_store_dir)

    directories = list(find_files(root_dir, 'GE.csv'))

    for directory in directories:
        print directory
        file_names = os.listdir(directory)

        for file_name in file_names:
            ticker = file_name[:len(file_name)-4]
            if '.' in ticker:
                ticker = ticker[:len(ticker)-2]

            frame = read_si_file(directory, file_name)
            print file_name
            try:
                first_date = si_store[ticker].index[0].value
                second_date = frame.index[0].value

                if first_date < second_date:
                    si_store[ticker] = si_store[ticker].combine_first(frame)
                else:
                    si_store[ticker] = frame.combine_first(si_store[ticker])
            except:
                si_store[ticker] = frame

    si_store.close()



if __name__ == "__main__":
    main(sys.argv)