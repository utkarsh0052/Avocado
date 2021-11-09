# -*- coding: utf-8 -*-
"""Avocado.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nzm9NK3AxsCeL6uwnkyNwKMQLOBiguIN

#Importing Libraries
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

"""##Loading Dataset"""

av_data = pd.read_csv('/Avocado.csv')

"""#Exploratory Data Analysis"""

av_data.head(10)

av_data.shape

"""###Check for Missing Values"""

av_data.isnull().sum()

av_data.describe()

"""######Conclusion: I usually take a look at the min and max values to identify outliers but I didn't find any this time."""

av_data.nunique()

av_data.columns

av_data = av_data.drop(['Unnamed: 0', 'year'], axis=1)
av_data.head(2)

av_data.count()

av_data.type.value_counts()

"""##### check for outliers"""

sns.boxplot(data = av_data)

av_data.boxplot(grid='false', color='blue',fontsize=10, rot=30)

av_data.value_counts()

av_data.region.value_counts()

"""##Data Visulization

######1. The average prices by regions
"""

plt.figure(figsize=(15,15))

plt.title("Avgerage Price of Avocado by Region")

sns.barplot(x="AveragePrice",y="region",data=av_data)

plt.show()



"""####2. The average prices of avocados by types"""

plt.figure(figsize=(5,7))

plt.title("Avg.Price of Avocados by Type")

sns.barplot(x="type",y="AveragePrice",data=av_data)

plt.show()



"""####3. Correlation"""

plt.figure(figsize=(12,6))
sns.heatmap(av_data.corr(),cmap='coolwarm',annot=True)

"""#####There is a high correlation between pairs:

4046 & total volume (0.98)
4225 & total volume (0.97)
4770 & total volume (0.87)
total bags & total volume (0.96)
small bags & total bags (0.99) etc

4046 avocados are the most preferred/sold type in the US and customers tend to buy those avocados as bulk, not bag.

Retailers want to increase the sales of bagged avocados instead of bulks. They think this is more advantageous for them.

Total Bags variable has a very high correlation with Total Volume (Total Sales) and Small Bags, so we can say that most of the bagged sales comes from the small bags
"""



"""#### Total vol."""

plt.figure(figsize=(12,6))
sns.boxplot(av_data['Total Volume'])

"""####Data Preperation
Let's get our data ready to use in our model selection. We need to do the following

create train and test splits
scale our numerical features
one-hot encode our categorical features
"""

from sklearn.model_selection import train_test_split

train, test = train_test_split(av_data,test_size = 0.20)

train_set, test_set = train_test_split(av_data, test_size=0.2, random_state=42)
train_set.shape, test_set.shape

train_features = train_set.drop("AveragePrice", axis=1)
train_labels = train_set["AveragePrice"].copy()

test_features = test_set.drop("AveragePrice", axis=1)
test_labels = test_set["AveragePrice"].copy()



from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

num_attribs = ['Total Volume', '4046', '4225', '4770', 'Total Bags','Small Bags', 'Large Bags', 'XLarge Bags']
cat_attribs = ['type', 'region']

num_pipline = Pipeline([('std_scaler', StandardScaler()),])
pipeline = ColumnTransformer([("num", num_pipline, num_attribs), ("cat", OneHotEncoder(), cat_attribs)])

train_prepared = pipeline.fit_transform(train_features)
train_prepared.toarray()[0]



"""##Model Selection
Let's just start off with simple linear regression, take a look of how it predicts off of some of our training data. Then Let's see with the RMSE value is. We see that our predictions do follow a line but perhaps not the best
"""

from sklearn.linear_model import LinearRegression


lin_reg = LinearRegression()
lin_reg.fit(train_prepared, train_labels)

some_data = train_features.iloc[:30]
some_data_prepared = pipeline.transform(some_data)
some_data_predicted = lin_reg.predict(some_data_prepared)
some_data_actual = train_labels.iloc[:30]

test_result = pd.DataFrame({
    'actual': list(some_data_actual),
    'predictions': list(some_data_predicted)
})

plt.scatter(test_result['actual'], test_result['predictions'])

from sklearn.metrics import mean_squared_error
pred = lin_reg.predict(train_prepared)
lin_mse = mean_squared_error(train_labels, pred)
lin_rmse = np.sqrt(lin_mse)
lin_rmse