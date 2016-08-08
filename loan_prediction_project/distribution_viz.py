# distribution_viz.py
# by Ryan Delgado July 12, 2016
# This script creates the histograms (for the continuous variables) and bar charts (for the ccounts of the categorical
# variables) of the Fannie Mae train.csv clean dataset.

import pandas as pd
import settings
import seaborn as sns

# Read in training dataset
train_df = pd.read_csv('%s/train.csv' % settings.PROCESSED_DIR, header=0)
#train_df = train_df[~train_df['foreclosure_status'].isnull()]

# Produce kde pair subplots of continuous variables
def kde_pair_subplot(ax, var_name, title):
    for tf in [True, False]:
        data = train_df.ix[train_df['foreclosure_status'] == tf, var_name]
        data = data[~data.isnull()]
        sns.kdeplot(data, legend=False, ax=ax)
    sns.plt.setp(ax.get_xticklabels(), rotation=45)
    ax.set_title(title)
    handles, labels = ax.get_legend_handles_labels()
    labels = ['Foreclosure', 'No Foreclosure']
    if (ax == ax1) or (ax == ax4) or (ax == ax5):
        ax.legend(handles, labels, loc='upper left')
    else:
        ax.legend(handles, labels)

f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = sns.plt.subplots(3,2)
kde_axs = [ax1, ax2, ax3, ax4, ax5, ax6]
kde_vars = ['borrower_credit_score', 'interest_rate', 'balance', 'cltv', 'dti']
kde_titles = ['Borrower Credit Score', 'Interest Rate', 'Balance', 'Combined Loan-to-Value', 'DTI']

for ax,var,title in zip(kde_axs, kde_vars, kde_titles):
    kde_pair_subplot(ax, var, title)

f.subplots_adjust(hspace=0.4, wspace=0.2)
f.set_size_inches(6, 4)
sns.plt.show()


cat_vars = ['channel','loan_purpose','first_time_homebuyer', 'borrower_count', 'occupancy_status']
groupby_frames = {}

for v in cat_vars:
    # Calculate the total count of each foreclosure_status & categorical variable combination
    groupby_frames[v] = train_df.groupby(['foreclosure_status',v])[v].count()

    # Calculate percentage share of foreclosure_status-level percentage of each facet of the categorical variable
    groupby_frames[v] =  groupby_frames[v].groupby(level=0).apply(lambda x: x/float(x.sum()))
    groupby_frames[v] = pd.DataFrame(groupby_frames[v])
    groupby_frames[v].columns = ['share']

    # Flatten groupby frame to prepare for bar plot
    groupby_frames[v] = groupby_frames[v].reset_index()

# Produce count bar charts for categorical variables
def share_bar_subplot(ax, var_name, title):
    data = groupby_frames[var_name]
    sns.barplot(x=var_name, y='share', hue='foreclosure_status', data=data, ax=ax)
    sns.plt.setp(ax.get_xticklabels(), rotation=45)

    # Set title and ylabel
    ax.set_title(title)
    ax.set_xlabel('')
    ax.set_ylabel('Share')

    # Set legends for each plot
    handles, labels = ax.get_legend_handles_labels()
    handles = handles[:2]
    labels = ['No Foreclosure','Foreclosure']
    if ax == ax1: # the legend in the first subplot will overlap with the bars if it's left in the upper right
        ax.legend(handles, labels, loc='upper left')
    else:
        ax.legend(handles, labels)


f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = sns.plt.subplots(3,2)
cat_axs = [ax1, ax2, ax3, ax4, ax5]
cat_titles = ['Channel', 'Loan Purpose', 'First Time Homebuyer', 'Borrower Count', 'occupancy_status']

for ax,var,title in zip(cat_axs, cat_vars, cat_titles):
    share_bar_subplot(ax,var,title)

f.subplots_adjust(hspace=0.5)
sns.plt.show()