#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Assuming df_train is your DataFrame
df_train = pd.read_csv("C:/Users/phill/OneDrive/Desktop/Portfolio/train.csv", sep=',')

# Drop 'id' column
df_train.drop(['id'], axis=1, inplace=True)

# Mapping for 'NObeyesdad'
df_train['NObeyesdad'] = df_train['NObeyesdad'].map({
    'Insufficient_Weight': 1,
    'Normal_Weight': 2,
    'Overweight_Level_I': 3,
    'Overweight_Level_II': 4,
    'Overweight_Level_III': 5,
    'Obesity_Type_I': 6,
    'Obesity_Type_II': 7,
    'Obesity_Type_III': 8
})

# Custom mapping for ordinal data
ordinal_mapping = {'Sometimes': 1, 'no': 2, 'Frequently': 3, 'Always': 4}
df_train['CAEC'] = df_train['CAEC'].map(ordinal_mapping)
df_train['CALC'] = df_train['CALC'].map(ordinal_mapping)

# Create a LabelEncoder
label_encoder = LabelEncoder()

# Iterate through columns and transform nominal data to numbers
for column in df_train.columns:
    if df_train[column].dtype == 'object':  # Check if the column contains nominal data
        df_train[column] = label_encoder.fit_transform(df_train[column])

# Feature Engineering: Convert weight to pounds, height to feet, and then calculate BMI
df_train['Weight_lbs'] = df_train['Weight'] * 2.20462  # Convert weight to pounds
df_train['Height_ft'] = df_train['Height'] * 0.0328084 * 100  # Convert height to feet
df_train['Height_inches'] = df_train['Height_ft'] * 12  # Convert height to inches

df_train['BMI'] = (df_train['Weight_lbs'] / (df_train['Height_inches'] ** 2))*703

# Create a new column 'beyesdad' based on BMI ranges
df_train['beyesdad'] = pd.cut(df_train['BMI'],
                                bins=[-float('inf'), 18.5, 24.9, 27.9, 29.9, 34.9, 39.9, float('inf')],
                                labels=['Insufficient_Weight', 'Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III'])

# Map the labels to numerical values
label_mapping = {
    'Insufficient_Weight': 1,
    'Normal_Weight': 2,
    'Overweight_Level_I': 3,
    'Overweight_Level_II': 4,
    'Obesity_Type_I': 5,
    'Obesity_Type_II': 6,
    'Obesity_Type_III': 7
}

df_train['BMI_Category'] = df_train['beyesdad'].map(label_mapping)

df_train = df_train.drop('beyesdad', axis=1)
df_train = df_train.drop('BMI_Category', axis=1)
df_train = df_train.drop('Weight_lbs', axis=1)
df_train = df_train.drop('Height_ft', axis=1)
df_train = df_train.drop('Height_inches', axis=1)

# Splitting into features (X) and target variable (Y)
X = df_train.drop('NObeyesdad', axis=1)
Y = df_train['NObeyesdad']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=1)

# Decision Tree
model_DT = tree.DecisionTreeClassifier(criterion='entropy')
model_DT.fit(X_train, y_train)
prediction_DT = model_DT.predict(X_test)
accuracy_DT = accuracy_score(y_test, prediction_DT)
print(f"Decision Tree Accuracy: {accuracy_DT:.4f}")

# Naive Bayes
model_NB = BernoulliNB()
model_NB.fit(X_train, y_train)
prediction_NB = model_NB.predict(X_test)
accuracy_NB = accuracy_score(y_test, prediction_NB)
print(f"Naive Bayes Accuracy: {accuracy_NB:.4f}")

# Random Forest
model_RF = RandomForestClassifier(n_estimators=100, random_state=1)
model_RF.fit(X_train, y_train)
prediction_RF = model_RF.predict(X_test)
accuracy_RF = accuracy_score(y_test, prediction_RF)
print(f"Random Forest Accuracy: {accuracy_RF:.4f}")

# Gradient Boosting
model_GB = GradientBoostingClassifier(n_estimators=100, random_state=1)
model_GB.fit(X_train, y_train)
prediction_GB = model_GB.predict(X_test)
accuracy_GB = accuracy_score(y_test, prediction_GB)
print(f"Gradient Boosting Accuracy: {accuracy_GB:.4f}")


#logistic Regression
df_train['BMI'] = df_train['Weight'] / ((df_train['Height'] / 100) ** 2)

# Splitting into features (X) and target variable (Y)
X = df_train.drop('NObeyesdad', axis=1)
Y = df_train['NObeyesdad']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=1)

# Logistic Regression for Classification
model_LogReg = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs')
model_LogReg.fit(X_train, y_train)

# Feature Engineering: Calculate BMI for test set
X_test['BMI'] = X_test['Weight'] / ((X_test['Height'] / 100) ** 2)

# Prediction using Logistic Regression
prediction_LogReg = model_LogReg.predict(X_test)

# Evaluation metrics for Logistic Regression
accuracy_LogReg = accuracy_score(y_test, prediction_LogReg)
classification_report_LogReg = classification_report(y_test, prediction_LogReg)
print(f"Logistic Regression Accuracy: {accuracy_LogReg:.4f}")
print(f"\nClassification Report:\n{classification_report_LogReg}")


# In[2]:


# So Random Forest is the most accurate and the one that we will use


# In[3]:


df_test = pd.read_csv("C:/Users/phill/OneDrive/Desktop/Portfolio/test.csv", sep=',')


# In[4]:


# Create a new DataFrame for 'id' column
df_id = df_test[['id']]

# Drop 'id' column
df_test.drop(['id'], axis=1, inplace=True)

# Feature Engineering: Convert weight to pounds, height to feet, and then calculate BMI
df_test['Weight_lbs'] = df_test['Weight'] * 2.20462  # Convert weight to pounds
df_test['Height_ft'] = df_test['Height'] * 0.0328084 * 100  # Convert height to feet
df_test['Height_inches'] = df_test['Height_ft'] * 12  # Convert height to inches

df_test['BMI'] = (df_test['Weight_lbs'] / (df_test['Height_inches'] ** 2))*703


df_test = df_test.drop('Weight_lbs', axis=1)
df_test = df_test.drop('Height_ft', axis=1)
df_test = df_test.drop('Height_inches', axis=1)

# Custom mapping for ordinal data
ordinal_mapping = {'Sometimes': 1, 'no': 2, 'Frequently': 3, 'Always': 4}
df_test['CAEC'] = df_test['CAEC'].map(ordinal_mapping)
df_test['CALC'] = df_test['CALC'].map(ordinal_mapping)




# Create a LabelEncoder
label_encoder = LabelEncoder()

# Iterate through columns and transform nominal data to numbers
for column in df_test.columns:
    if df_test[column].dtype == 'object':  # Check if the column contains nominal data
        df_test[column] = label_encoder.fit_transform(df_test[column])
        


# In[5]:


# Model Stage

# Random Forest
model_RF = RandomForestClassifier(n_estimators=100, random_state=1)
model_RF.fit(X, Y)
prediction_RF = model_RF.predict(df_test)

df = pd.DataFrame(prediction_RF, columns = ["NObeyesdad"])


# In[6]:


reverse_mapping = {
    1: 'Insufficient_Weight',
    2: 'Normal_Weight',
    3: 'Overweight_Level_I',
    4: 'Overweight_Level_II',
    5: 'Overweight_Level_III',
    6: 'Obesity_Type_I',
    7: 'Obesity_Type_II',
    8: 'Obesity_Type_III'
}

# Revert the mapping
df['NObeyesdad'] = df['NObeyesdad'].replace(reverse_mapping)

df_combined = pd.concat([df_id, df], axis=1)
df_combined


# In[7]:


#df_combined.to_csv('Obesity.csv', index = False)

