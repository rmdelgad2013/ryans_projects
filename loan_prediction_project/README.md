Loan Prediction Project
===

This project uses uses machine learning algorithms to predict the probability of foreclosure given 
attributes about the borrower. It uses the Fannie Mae Acquisition & Performance datasets available
publicly on their website. This project will predict the probability of foreclosure using Logistic
Regression (via the Scikit-learn package) and an Artificial Neural Network (via the TFLearn wrapper
for the Tensor Flow deep learning package). The performance of both models will be compared.


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

--- README.md

--- requirements.txt

--- settings.py

--- clean_performance.py


_Note: The data files are not uploaded to the repository to save space. The raw data can be downloaded
from their website, and the processed data can be produced by running the scripts_