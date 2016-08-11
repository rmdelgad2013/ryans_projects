# log_ret
# by Ryan Delgado 8/8/2016
# This script implements several Logistic Regression models for predicting whether a borrower defaults on a mortgage.
# The models are compared, and a "best" model is decided on.

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.cross_validation import cross_val_predict
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

# Create a LogRet model, then cross validate the model on the training dataset using cross_val_predict
logistic_model = LogisticRegression(class_weight='balanced')
logistic_predictions = cross_val_predict(logistic_model, train_df[features], train_df[label], cv=4)

# Evaluate logistic regression model with accuracy score, a confusion matrix, and a classification report
print('Logistic Regression Accuracy Score: %s' %metrics.accuracy_score(train_df[label], logistic_predictions))

print('Logistic Regression Confusion Matrix:')
print(metrics.confusion_matrix(train_df[label], logistic_predictions))

print('Logistic Regression Classification Report:')
print(metrics.classification_report(logistic_predictions, train_df[label]))

# It looks like our logistic regression model is right about 75% of the time. Let's try a Random Forest predictive model
# to see if we can improve our results.
forest_model = RandomForestClassifier(max_depth=10, n_estimators=40, class_weight='balanced')
forest_predictions = cross_val_predict(forest_model, train_df[features], train_df[label], cv=4)

# Evaluate logistic regression model with accuracy score, a confusion matrix, and a classification report
print('Random Forest Accuracy Score: %s' %metrics.accuracy_score(train_df[label], forest_predictions))

print('Random Forest Confusion Matrix:')
print(metrics.confusion_matrix(train_df[label], forest_predictions))

print('Random Forest Classification Report:')
print(metrics.classification_report(forest_predictions, train_df[label]))