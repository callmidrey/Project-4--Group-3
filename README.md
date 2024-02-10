# Project-4--Group-3
Bootcamp Project 4- Project Title: Analyzing Home Credit Default Risk

# Introduction
This Project was conducted b 4 group members in the Data Analytics Bootcamp with the University of Toronto School of Continus Studies. The group members are Lovepreet Singh, Muhammad Kashif, Vinay Vattipally and Audrey Nkrumah.

Introduction to the Home Credit Default Risk dataset.

Objectives and goals of the analysis.
The objective of the project is to :
1. Exploratory Data Analysis (EDA):
        Understand the distribution and relationships between variables in the dataset.
        Identify trends, patterns, and outliers.
        Explore correlations between features and the target variable.
        Visualize key insights to gain a better understanding of the data.

2. Feature Importance Analysis:
        Determine which features have the most significant impact on predicting default risk.
        Use techniques like feature importance scores from machine learning models or statistical methods to rank features.

3. Risk Segmentation:
        Identify different risk segments within the dataset based on demographic or financial characteristics.
        Analyze the characteristics of high-risk and low-risk groups.
        Develop strategies to mitigate risk for different segments.

4. Customer Profiling:
        Create profiles of different types of customers based on their credit behavior, demographic information, and financial history.
        Understand the characteristics of customers who are more likely to default on their loans.         

5. Build a good predictive model and Interprate the Model to:
        Understand how the predictive model makes decisions.
        Interpret model coefficients, feature importance scores, or other model outputs to explain predictions.
        Identify factors contributing to high or low default probabilities for individual borrowers.

# Data Understanding

Description of the dataset: features, target variable, etc.<br>
#### Data source and acquisition process.<br>
- Data is acquired from Kaggle.com provided by Home credit Group.<br>
- Data contains files:
<ul>
        <li>application_{train|test}.csv</li>
        <li>bureau.csv</li>
        <li>bureau_balance.csv</li>
        <li>POS_CASH_balance.csv</li>
        <li>credit_card_balance.csv</li>
        <li>previous_application.csv</li>
        <li>installments_payments.csv</li>
        <li>HomeCredit_columns_description.csv</li>     
</ul>

### Data preprocessing steps:<br>
#### Handling missing values.<br>
- Data obtained from source has categorical data in refined form.e.g. minimal bad entries.
- However Null values in were filled by putting 0 values in columns where 0 and 1 does not impact our model predictions. since model predictions are binary which can lead to model inaccurate predictions.<br>
#### Data cleaning and formatting.<br>
- After Initial cleaning and handling of missing values, CSV files are exported.<br>
#### Connect to Sources(APIs):<br>
- APIs are created using Database queries, Final schema file is used to create tables in Postgresql. Tables are populated with data by using postgresqlpop.ipynb file which have functions to insert data in the database from CSV files.<br>
app.py file has query setup to obtain data from Postgresql via APIs. <br>
below is list of APIs:<br>
<ul>
        <li>"Bureau" : 'http://127.0.0.1:5000/bureau'</li>
       <li>"Bureau_balance" : 'http://127.0.0.1:5000/bureau_balance'</li>
        <li>"Credit_card_balance" : 'http://127.0.0.1:5000/credit_card_balance'</li>
        <li>"Installments_payments" : 'http://127.0.0.1:5000/installments_payments'</li>
       <li>"POS_CASH_balance" : 'http://127.0.0.1:5000/pOS_CASH_balance',</li>
       <li> "Previous_application" : 'http://127.0.0.1:5000/previous_application'</li>
        <li>"Application_train" : 'http://127.0.0.1:5000/application_train'</li>
</ul>

#### Data Retrieval from APIs:<br>
- Data is extracted from API and tables are merged together using get_data_from_api.ipynb file.
- Data is then used for modelling process and Data analysis.
- Exploratory Data Analysis (EDA).
- Summary statistics.
- Data visualization (histograms, box plots, correlation matrices, etc.).

#### Feature Engineering
- Creation of new features (if applicable).
- Encoding categorical variables.
- Feature selection techniques.
- Scaling and normalization of numerical features.

#### Model Building
1. Model accuracy & probability
- Splitting the dataset into training and testing sets.
- Selection of appropriate machine learning algorithms: Random Forest Classifier. 
- Model training and evaluation.
- Performance metrics (accuracy, precision, recall, F1-score, etc.).

![Alt text](image-2.png)

- Hyperparameter tuning.
- Choosing top contributing features in model and testing model accuracy again.

![Alt text](image-3.png)


2. Model prediction
- Splitting the dataset into training and testing sets.
- Selection of appropriate machine learning algorithms: Random Forest Regressor, XG Boost, Lasso Regression and Neural Network Regression.
- Model training and evaluation.
- Performance metrics (accuracy, precision, recall, F1-score, etc.).

![Alt text](image-1.png)

- Hyperparameter tuning.

#### Website Building

 

# Results and Discussion
- Presentation of the model evaluation results.
- Interpretation of feature importance.
- Discussion on the model's performance and limitations.
- Insights derived from the analysis.

# Conclusion
- Summary of key findings.
- Recommendations for future work.
- Conclusion remarks.

# References
- Citation of datasets, libraries, and resources used.
Data Source: https://www.kaggle.com/c/home-credit-default-risk/data
# Appendix
- Additional charts or tables.
- Any other supplementary materials.


