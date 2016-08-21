Loan Prediction Project
===

This project explores the lona acquisition variables that predict the probability 
of defaultuses uses machine learning algorithms to predict the probability of foreclosure given 
attributes about the borrower. It uses the Fannie Mae Acquisition & Performance datasets available
publicly on their website. This project will predict the probability of foreclosure using Logistic
Regression and Random Forests (via  Scikit-learn). The performance of both models will be compared.


**Project structure**

loan_prediction_project

--- raw_data

------ Acquisition_2012Q1.txt

------ Acquisition_2012Q2.txt

------ Performance_2012Q1.txt

------ Performance_2012Q2.txt

------ ...

--- processed_data

------ Acquisition.csv

------ Performance.csv

------ train.csv

--- assemble_acquisition.py

--- classifier_cross_val.py

--- clean_performance.py

--- create_train.py

--- distribution_viz.py

--- fanniemae_prediction.ipynb

--- README.md

--- requirements.txt

--- settings.py


_Note: The data files are not uploaded to the repository to save space. The raw data can be downloaded
from Fannie Mae's website, and the processed data can be produced by running the scripts._