# assemble_acquisition.py
# written by Ryan Delgado
# This script combines the Acquisition data into one csv filee.

import os
import settings
import pandas as pd

# List Acquisition columns we want to keep
acq_columns = [
        "id",
        "channel",
        "seller",
        "interest_rate",
        "balance",
        "loan_term",
        "origination_date",
        "first_payment_date",
        "ltv",
        "cltv",
        "borrower_count",
        "dti",
        "borrower_credit_score",
        "first_time_homebuyer",
        "loan_purpose",
        "property_type",
        "unit_count",
        "occupancy_status",
        "property_state",
        "zip",
        "insurance_percentage",
        "product_type",
        "co_borrower_credit_score"
    ]

files = os.listdir(settings.DATA_DIR)

# Read in each Acquisition file into a list of DataFrames, then concatenate all DataFrames into one DataFrame
full = []
for f in files:
    if not f.startswith('Acquisition'):
        continue
    print('Reading file %s' % f)
    data = pd.read_csv(os.path.join(settings.DATA_DIR, f), sep="|", header=None, names=acq_columns, index_col=False)
    data = data[acq_columns]
    full.append(data)

full = pd.concat(full, axis=0)

# Write to csv file in the processed_data directory
print("Writing file %s" % os.path.join(settings.PROCESSED_DIR, "{}.csv".format('Acquisition')))
full.to_csv(os.path.join(settings.PROCESSED_DIR, "{}.csv".format('Acquisition')), header=acq_columns, index=False)

