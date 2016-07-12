# settings.py
# Initial settings script to set up the project. This module will be imported by all of the scripts
# by Ryan Delgado 7/9/2016

DATA_DIR = "raw_data"
PROCESSED_DIR = "processed_data"
MINIMUM_TRACKING_QUARTERS = 4
TARGET = "foreclosure_status"
NON_PREDICTORS = [TARGET, "id"]
CV_FOLDS = 3
