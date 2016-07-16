# create_train.py
# by Ryan Delgado July 16, 2016
# This script joins the Acquisition & Performance CSV files and removes missing values.

import pandas as pd
import settings

# Read datasets into DataFrames
acq_df = pd.read_csv('%s/Acquisition.csv' % settings.PROCESSED_DIR)
prf_df = pd.read_csv('%s/Performance.csv' % settings.PROCESSED_DIR)

# Inner-join on id
train_df = acq_df.merge(prf_df, how='inner', on='id')

# List number of missing values for each column and total
print('Number of missing values in each column:')
print(train_df.isnull().sum())

# Remove rows with missing values for cltv, borrower_count, dti, and borrower_credit_score
train_df = train_df.dropna(subset=['cltv','borrower_count','dti','borrower_credit_score'])

# Write to train.csv
train_df.to_csv('%s/train.csv' % settings.PROCESSED_DIR, index=False)