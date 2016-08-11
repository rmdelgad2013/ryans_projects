# create_train.py
# by Ryan Delgado July 16, 2016
# This script joins the Acquisition & Performance CSV files and removes missing values.

import pandas as pd
import numpy as np
import settings
from sklearn.cross_validation import train_test_split

# Read datasets into DataFrames
acq_df = pd.read_csv('%s/Acquisition.csv' % settings.PROCESSED_DIR)
prf_df = pd.read_csv('%s/Performance.csv' % settings.PROCESSED_DIR)

# Inner-join on id
fannie_df = acq_df.merge(prf_df, how='inner', on='id')

# List number of missing values for each column and total
print('Number of missing values in each column:')
print(fannie_df.isnull().sum())

# Remove rows with missing values for cltv, borrower_count, dti, and borrower_credit_score
fannie_df = fannie_df.dropna(subset=['cltv','borrower_count','dti','borrower_credit_score'])

# Remove rows where loan_purpose = U, or where first_time_homebuyer = U
fannie_df = fannie_df[fannie_df['loan_purpose'] != 'U']
fannie_df = fannie_df[fannie_df['first_time_homebuyer'] != 'U']

# Create categorical variable for single_borrower
fannie_df['single_borrower'] = 'Y'
fannie_df.ix[fannie_df['borrower_count'] > 1,'single_borrower'] = 'N'

# Create categorical dummy features for each categorical variable. Add categorical features to training dataset
categorical_vars = ['first_time_homebuyer','channel','loan_purpose',
                    'single_borrower', 'occupancy_status', 'foreclosure_status']

for var in categorical_vars:
    dum = pd.get_dummies(fannie_df[var], prefix=var)
    fannie_df = pd.concat([fannie_df, dum], axis=1)

# Create score/cltv feature, as suggested by the Fannie Mae 102 presentation
fannie_df['score_div_cltv'] = fannie_df['borrower_credit_score'] / fannie_df['cltv']

# Create log(balance) feature
fannie_df['balance_log'] = np.log(fannie_df['balance'])

# Separate into train/test
train_df, test_df = train_test_split(fannie_df, test_size=0.1)

# Write to train.csv
train_df.to_csv('%s/train.csv' % settings.PROCESSED_DIR, index=False)
test_df.to_csv('%s/test.csv' % settings.PROCESSED_DIR, index=False)