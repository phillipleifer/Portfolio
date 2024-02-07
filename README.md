# Welcome to Phillip Leifer Data Analytics Portfolio
Welcome to my GitHub portfolio! I'm Phillip Leifer, a results-driven data professional with a strong mix of analytical techniques and business acumen. With a Master's degree in Business Analytics from Florida State University and a Bachelor's degree in Finance and Accounting from Utah State University, I have honed my skills in data analysis, visualization, and modeling to deliver data-driven solutions that optimize business processes.

## About Me
With a master's degree in business analytics, I possess a robust background in data science, statistics, and business intelligence, enabling me to tackle intricate business challenges effectively. My experience spans roles such as a crediting analyst at Qualtrics, where I optimized contract creation processes and provided technical support to sales teams, leveraging advanced functionalities of Google Sheets for billing calculations and reporting. Additionally, during my tenure at the U.S. Nuclear Regulatory Commission as a financial analyst, I developed Tableau dashboards to monitor KPIs and expenditure trends, while implementing workflow solutions resulting in significant time savings for contract processing.

Driven by a passion for aiding others and enhancing organizational efficiency, I am committed to continual personal and professional growth. Seeking an analytical role where I can utilize my expertise in Python, R, Tableau, and other tools to contribute to an organization's success, I am dedicated to achieving and surpassing goals to facilitate both personal development and business advancement.

## Skills
**Programming**: Python (Pandas, Numpy, Scikit-Learn, Matplotlib, Seaborn), R (dplyr, ggplot2, data.table)

**Databases**: MySQL

**Visualization Tools**: Tableau, Microsoft Power BI, Excel

**Other Tools**: Smartsheet, NetSuite, Salesforce

## Portfolio Overview
This portfolio showcases a collection of projects that highlight my expertise in data analytics, visualization, and modeling. Each project demonstrates my ability to clean, analyze, and visualize data to uncover meaningful insights and drive informed decision-making.

Here's a brief overview of the projects included in this portfolio:

### Stock App:
Leveraging Python (Django, Flask), HTML, and CSS, I developed a website to predict and analyze stock performance, demonstrating my skills in data science.

**Data Retrieval and Analysis**:
This project harnesses the Yahoo Finance API (yfinance) to retrieve historical stock data for a specified symbol over a defined time frame. Leveraging this data, the script computes vital financial metrics crucial for evaluating stock performance:

**Arithmetic and Geometric Averages of Returns**: Offering insights into the average return achieved over the specified time frame, considering various calculation methodologies.
**Standard Deviations**: Quantifying the volatility or risk associated with the stock's returns.
Sharpe Ratio: Serving as a measure of the risk-adjusted return, providing a gauge of the return generated per unit of risk taken.
Beta: Representing the stock's sensitivity to market movements, indicating the extent to which the stock's returns tend to move relative to the overall market.

**Construction of Analysis DataFrame**:
After computing these metrics, the script organizes them into a structured DataFrame. This DataFrame serves as a concise summary of the single stock's performance, facilitating easier interpretation. Additionally, the script calculates the expected return and confidence intervals based on the standard deviation. These intervals (68%, 95%, and 97%) offer valuable insights into the range within which the actual returns are likely to fall, considering the stock's historical volatility.

**Visualization**:
To augment the presentation of the analysis, the script generates HTML tables displaying both the stock analysis metrics and standard deviation intervals. This HTML format allows for seamless integration into various platforms, such as websites or reports. Furthermore, the script employs the plot_historical_data() function to create a visual representation of the stock's historical performance. This plot compares the stock's adjusted closing prices with those of the market index (S&P 500), offering a graphical perspective on the stock's performance relative to the broader market.

<img width="1121" alt="image" src="https://github.com/phillipleifer/Portfolio/assets/89884799/be1e291d-21c9-416e-b6a8-b0d4f95d2659">

<img width="1114" alt="image" src="https://github.com/phillipleifer/Portfolio/assets/89884799/293165c0-1391-4777-b35c-570a76732fab">

 **Optimization**:
This stock app goes beyond single stock analysis by integrating portfolio metrics. Users have the flexibility to delve into calculations for equal-weighted stocks, custom-weighted stocks, and optimized weights, with the Sharpe ratio serving as the optimized metric. This functionality enables users to thoroughly analyze and customize their portfolios to suit their investment preferences effectively.

<img width="1121" alt="image" src="https://github.com/phillipleifer/Portfolio/assets/89884799/d4fd4d14-3814-4b6d-8cb9-43b24fd92c96">

In summary, this project showcases proficiency in financial data analysis, leveraging Python libraries to extract, analyze, and visualize historical stock data. By presenting key performance metrics and confidence intervals clearly and visually, this project demonstrates the ability to derive meaningful insights essential for informed investment decision-making.


### Obesity Data Modeling: 
Using Python (Pandas, NumPy, Scikit-Learn) and statistical analysis techniques, I conducted data modeling to address challenges in obesity research, showcasing my proficiency in data mining, engineering, and modeling.

**Project Objective**:
In this project, I aimed to predict the level of obesity based on various health-related attributes. Here's a breakdown of my approach:

**Data Exploration and Cleaning**: I began by loading the dataset using Pandas and dropping unnecessary columns like 'id'. Next, I transformed the target variable 'NObeyesdad' into numerical categories for ease of modeling.

**Feature Engineering**: Recognizing the importance of feature engineering in predictive modeling, I converted categorical ordinal variables like 'CAEC' and 'CALC' into numerical representations. Additionally, I engineered a new feature, Body Mass Index (BMI), which is a commonly used indicator of healthy weight. This involved converting weight to pounds, height to feet, and then calculating the BMI.

**Model Selection and Training**:

**Decision Tree**: I trained a Decision Tree classifier with entropy criterion, achieving an accuracy of 85.37%.
**Naive Bayes**: Next, I employed a Bernoulli Naive Bayes classifier, yielding an accuracy of 49.05%.
**Random Forest**: Given its high accuracy of 90.30%, I utilized a Random Forest classifier with 100 estimators for robust prediction.
**Gradient Boosting**: Using Gradient Boosting with 100 estimators, I attained a competitive accuracy of 90.09%.
**Logistic Regression**: Despite its relatively low accuracy of 20.30%, I also implemented Logistic Regression for comparison.

**Testing Dataset Prediction**: Leveraging the Random Forest model due to its superior accuracy, I applied it to predict the level of obesity in a testing dataset. After preprocessing the test data, I made predictions and transformed the results back into meaningful categories. Finally, I combined the predictions with their respective IDs for submission.

In summary, this portfolio entry showcases proficiency in machine learning techniques and data preprocessing, emphasizing the importance of informed decisions in model selection and feature engineering. These skills are essential for achieving accurate predictions in real-world scenarios, highlighting the ability to tackle complex data challenges effectively.


### SQL Project: 
I implemented SQL queries to analyze and extract insights from large datasets, demonstrating my expertise in database management and querying.

**File 1**: Managing Charity Auction Data

This SQL file demonstrates proficiency in handling and analyzing charity auction data spanning four years. Initially, the file splits the data into separate tables for each year, ensuring organization and ease of analysis. It then identifies new and returning bidders, a critical task in understanding attendee dynamics. Through various SQL operations such as joins, subqueries, and conditional statements, the file creates both wide and long-format datasets, catering to different analytical needs. These operations showcase versatility and adeptness in manipulating data structures. Furthermore, the file highlights the importance of data completeness by addressing missing values and ensuring uniformity across datasets. Overall, it reflects strong SQL skills in data management and analysis, essential for extracting meaningful insights from complex datasets.

**File 2**: Integrating U.S. County Data

This SQL file illustrates the integration of diverse datasets related to U.S. counties, including poverty and unemployment rates, Medicaid expansion information, and county adjacency data. It begins by combining poverty and unemployment rates for each county, emphasizing data quality and consistency through inner joins. The file then appends Medicaid expansion information, providing valuable context for socioeconomic analysis. Through advanced SQL techniques like cross joins and left joins, it constructs comprehensive datasets that facilitate in-depth analysis of county-level economic indicators. Moreover, the file showcases problem-solving skills in addressing data gaps and handling complex relationships between datasets. Overall, it showcases proficiency in SQL data integration and analysis, essential for informed decision-making in socioeconomic research and policy planning.

These tasks allowed me to learn and implement SQL coding effectively, showcasing my ability to tackle data challenges and derive actionable insights. Through these projects, I honed my skills in database management, query optimization, and data integration, positioning myself as a competent data analyst capable of driving informed decision-making processes in various domains.


### Tableau Visualization: 
Leveraging Tableau and Microsoft Power BI, I created interactive visualizations to communicate insights and trends effectively, highlighting my skills in data visualization and storytelling.

I have submitted two files showcasing my proficiency in Tableau. These documents serve as a testament to my skills and capabilities within the platform. Should you be interested in reviewing them. They encapsulate my ability to manipulate data effectively, design insightful visualizations, and derive meaningful insights to aid decision-making processes.


Feel free to explore each project folder to delve deeper into the details. I'm always open to feedback, collaboration opportunities, and discussions about data analytics and its applications.

Thank you for visiting my portfolio!

