# log_ret
# by Ryan Delgado 8/8/2016
# This script implements several Logistic Regression models for predicting whether a borrower defaults on a mortgage.
# The models are compared, and a "best" model is decided on.

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import statsmodels.api as sm
import settings


# Import training dataset and select features and label for logistic regression
train_df = pd.read_csv('%s/train.csv' % settings.PROCESSED_DIR)
test_df = pd.read_csv('%s/test.csv' % settings.PROCESSED_DIR)

label = 'foreclosure_status_True'
features = ['score_div_cltv','borrower_credit_score','cltv','interest_rate', 'dti', 'balance_log', 'first_time_homebuyer_Y',
            'channel_C','channel_R', 'loan_purpose_C','loan_purpose_P', 'single_borrower_Y', 'occupancy_status_I',
            'occupancy_status_P']

# Perform an initial logistic regression with statsmodels & the train_df frame to test the significance of each feature.
# This is just to slake my econometric taste. :)
logit = sm.Logit(train_df[label], sm.add_constant(train_df[features]))
result = logit.fit()
result.summary()

# Use train_df & sklearn to fit a LogRet model
logistic_model = LogisticRegression(class_weight='balanced')
logistic_model.fit(train_df[features], train_df[label])

# Predict foreclosure_status_Y in test_df using the trained logistic model
logit_predictions = logistic_model.predict(test_df[features])

# Produce a classification report
print(classification_report(logit_predictions, test_df[label]))
print(confusion_matrix(test_df[label], logit_predictions))

# It looks like our logistic regression model is right about 75% of the time. Let's try a Random Forest predictive model
# to see if we can improve our results.

rf = RandomForestClassifier(max_depth=10, n_estimators=100, class_weight='balanced')
rf.fit(train_df[features], train_df[label])
rf_predictions = rf.predict(test_df[features])

print(classification_report(rf_predictions, test_df[label]))
print(confusion_matrix(test_df[label], rf_predictions))



