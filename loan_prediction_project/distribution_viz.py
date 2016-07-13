# distribution_viz.py
# by Ryan Delgado July 12, 2016
# This script creates the histograms (for the continuous variables) and bar charts (for the ccounts of the categorical
# variables) of the Fannie Mae train.csv clean dataset.

import pandas as pd
import settings
import seaborn as sns
import matplotlib.pyplot as plt

train_df = pd.read_csv('%s/train.csv' % settings.PROCESSED_DIR, header=0)
train_df = train_df[~train_df['foreclosure_status'].isnull()]

# Produce kde pair subplots of continuous variables
def kde_pair_subplot(ax, var_name, title):
    for tf,clr in zip([True, False],['r','g']):
        data = train_df.ix[train_df['foreclosure_status'] == tf, var_name]
        data = data[~data.isnull()]
        sns.kdeplot(data, color=clr, legend=False, ax=ax)
    sns.plt.setp(ax.get_xticklabels(), rotation=45)
    ax.set_title(title)

f, ((ax1, ax2), (ax3, ax4)) = sns.plt.subplots(2,2)
kde_axs = [ax1, ax2, ax3, ax4]
kde_vars = ['borrower_credit_score', 'interest_rate', 'balance', 'cltv']
kde_titles = ['Borrower Credit Score', 'Interest Rate', 'Balance', 'Combined Loan-to-Value']

for ax,var,title in zip(kde_axs, kde_vars, kde_titles):
    kde_pair_subplot(ax, var, title)

sns.plt.show()

# Produce count bar charts for categorical variables
def count_bar_pair_subplots(ax, var_name, title):
    for tf,clr in zip([True, False],['r','g']):
        pass
    sns.plt.setp(ax.get_xticklabels(), rotation=45)
    ax.set_title(title)
