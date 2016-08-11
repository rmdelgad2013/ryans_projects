# create_train.py
# by Ryan Delgado July 16, 2016
# This script joins the Acquisition & Performance CSV files and removes missing values.

import pandas as pd
import numpy as np
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

# Remove rows where loan_purpose = U, or where first_time_homebuyer = U
train_df = train_df[train_df['loan_purpose'] != 'U']
train_df = train_df[train_df['first_time_homebuyer'] != 'U']

# Create categorical variable for single_borrower
train_df['single_borrower'] = 'Y'
train_df.ix[train_df['borrower_count'] > 1,'single_borrower'] = 'N'

# Create categorical dummy features for each categorical variable. Add categorical features to training dataset
categorical_vars = ['first_time_homebuyer','channel','loan_purpose',
                    'single_borrower', 'occupancy_status', 'foreclosure_status']

for var in categorical_vars:
    dum = pd.get_dummies(train_df[var], prefix=var)
    train_df = pd.concat([train_df, dum], axis=1)

# Create score/cltv feature, as suggested by the Fannie Mae 102 presentation
train_df['score_div_cltv'] = train_df['borrower_credit_score'] / train_df['cltv']

# Create log(balance) feature
train_df['balance_log'] = np.log(train_df['balance'])

# Separate into train/test

# Write to train.csv
train_df.to_csv('%s/train.csv' % settings.PROCESSED_DIR, index=False)
