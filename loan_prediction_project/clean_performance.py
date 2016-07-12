# clean_performance.py
# by Ryan Delgado July 11, 2016
# The purpose of this script is to clean the FannieMae performance data. The performance data needs to be set up for a
# classification problem, so it needs to be transformed into a smaller table with 3 columns: unique ID, foreclosed? 0 or 1,
# and the date of foreclosure (if the second column = 1).

import os
import settings
import pandas as pd

def count_performance_rows(perf_file, counts={}):
    with open(os.path.join(settings.DATA_DIR, perf_file), 'r') as f:
        for i, line in enumerate(f):
            try:
                if i == 0:
                    continue
                row = line.split('|')
                loan_id = int(row[0])
                if loan_id not in counts:
                    counts[loan_id] = {
                        'foreclosure_status': False,
                        'performance_count': 0
                    }

                # Increment the number of quarters this loan has been open for
                counts[loan_id]["performance_count"] += 1

                # If the foreclosure_date entry is non-empty, then the loan has been foreclosed on
                if len(row[14].strip()) > 0:
                    counts[loan_id]["foreclosure_status"] = True
            except ValueError:
                continue

    return counts


files = os.listdir(settings.DATA_DIR)

counts = {}
for f in files:
    if not f.startswith('Performance'):
        continue

    print('Reading file %s' % f)
    counts = count_performance_rows(f, counts=counts)

counts = pd.DataFrame.from_dict(counts, orient='index')
counts.to_csv(os.path.join(settings.PROCESSED_DIR,'Performance.csv'))