import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


# 
# ### 1.1: Reporting number of COVID-19 cases in each London local authority
# First, read the “cases.csv” dataset into a dataframe. Create a new dataframe where rows are the unique names of London local authorities and the columns are the total number of covid cases in each London local authority (include both count columns in the starting dataframe).



# Reading the csv file
df_cases=pd.read_csv("cases.csv",sep=",")

# Previewing the first few lines of the data
df_cases.head()



# Assumption: The geographical locations have similar population size for as estimated number for covid_19_deaths_per_thousand column, since population data is from mid 2018 which may vary from the actual 2020 numbers.
new_df_cases=df_cases.groupby('Local authority',as_index=False).agg({'covid_19_deaths':'sum','covid_19_deaths_per_thousand':'mean'})
new_df_cases.head()


# ### 1.2: Calculating percentage of COVID-19 cases in each London local authority
# Read the “population.csv” dataset and calculate the percentage of covid cases in each city of London region according to the total population and add it as a new column to the datafame. Sort the dataframe according to this column.
# 



df_population=pd.read_csv('population.csv')
df_population.head()

# Assumption: The geographical locations have similar population size for as estimated number for the over_70_prop column.

new_df_population=df_population.groupby('Local authority',as_index=False).agg({'total_population_mid_2018':'sum','over_70_prop':'mean'})
new_df_population.head()
new_df_cases=pd.merge(new_df_cases,new_df_population,on='Local authority',how='outer')
new_df_cases.head()


# Adding percentage_of_cases column with unit %
new_df_cases['percentage_of_cases(%)']=new_df_cases['covid_19_deaths']/new_df_cases['total_population_mid_2018']*100

# Sorted the column in descending order to see Local authorities with the highest percentage of cases
new_df_cases=new_df_cases.sort_values('percentage_of_cases(%)',ascending=False)
new_df_cases.head()


# ### 1.3: Finding the largest and smallest population based on ethnicity group in each city of London
# Read the “ethnic.csv” dataset and calculate the population of different ethnicity groups in each London borough using column “total\_population\_mid\_2018” from the first dataset “cases.csv”. Plot a bar chart to compare cases in each ethnicity group for each London local authority.



df_ethnic=pd.read_csv('ethnic.csv',sep=',')
# df_ethnic = df_ethnic.rename(columns={'Local Authority': 'Local authority'})

ethnicity_by_boroughs=df_ethnic[['all_bame_prop','all_black_prop','pakistani_or_bangladeshi_prop','all_indian_prop']].multiply(df_population['total_population_mid_2018'],axis=0)

ethnicity_by_boroughs=ethnicity_by_boroughs.rename(columns={'all_bame_prop':'bame_population','all_black_prop':'black_population','pakistani_or_bangladeshi_prop':'pakistani_bangladeshi_population','all_indian_prop':'indian_population'})
ethnicity_by_boroughs.insert(0,'Local Authority',df_ethnic['Local Authority'])
ethnicity_by_boroughs=ethnicity_by_boroughs.groupby('Local Authority',as_index=False).sum()

# Calculating the population of other minorities within BAME who are not black, pakistani or bangladeshi, or indian.
ethnicity_by_boroughs['other_minority_population']=ethnicity_by_boroughs['bame_population']-ethnicity_by_boroughs['black_population']-ethnicity_by_boroughs['pakistani_bangladeshi_population']-ethnicity_by_boroughs['indian_population']
ethnicity_by_boroughs.head()



# Excluding the white population under the assumption that this chart is just to analyse the population of minority groups in London local authority.
# Excluding BAME population column from this chart as the total population plotted, i.e. black, pakistani & bangladeshi, indian and other minorities, add up to the total BAME population.
ethnicity_chart=ethnicity_by_boroughs.plot.bar(x='Local Authority',y=['black_population','pakistani_bangladeshi_population','indian_population','other_minority_population'],title='Population of ethnic groups by London local authorities',figsize=(20,10),stacked=True)
ethnicity_chart.set_ylabel("Population")
# Assuming that the intention of this chart is to understand if there is a disporportionate impact of the virus against minorities, it would be helpful to have the covid cases data by each ethnic group.


# ### 1-4: Analysing the medical conditions of each region 
# Read the “medical.csv” dataset. Calculate total percentage of patients with “Hypertension”, “Obesity (18+)”, “Diabetes”, “Asthma”, and “Coronary heart disease” for each London local authority. For each medical condition, draw a boxplot of medical case frequencies for the 5 regions with the highest "total\_registered\_patient". Then, add a new column to the daraframe from section 1.2 to show the medical conditions with the highest number patients in each London borough.  



df_medical=pd.read_csv('medical.csv',sep=',')
# Assuming that the data for each medical conditions is independent from each other.
medical_condition_population=df_medical[['Hypertension','Obesity (18+)','Diabetes','Asthma','Coronary heart disease']].multiply(df_medical['total_registered_patients'],axis=0)
# Dividing the population by 100 as previous numbers were in percentages and not proportions.
medical_condition_population=medical_condition_population/100

# Adding the Local Authority and Total registered patients columns for analysis - to groupby Local authority and calculate the percentage of the medical conditions by local authority
medical_condition_population.insert(0,'Local authority',df_medical['Local authority'])
medical_condition_population.insert(1,'total_registered_patients',df_medical['total_registered_patients'])
medical_condition_population=medical_condition_population.groupby('Local authority',as_index=False).sum()
# Calculating the total percentages for each medical condition by local authority
medical_condition_population['Hypertension']=medical_condition_population['Hypertension']/medical_condition_population['total_registered_patients']*100
medical_condition_population['Obesity (18+)']=medical_condition_population['Obesity (18+)']/medical_condition_population['total_registered_patients']*100
medical_condition_population['Diabetes']=medical_condition_population['Diabetes']/medical_condition_population['total_registered_patients']*100
medical_condition_population['Asthma']=medical_condition_population['Asthma']/medical_condition_population['total_registered_patients']*100
medical_condition_population['Coronary heart disease']=medical_condition_population['Coronary heart disease']/medical_condition_population['total_registered_patients']*100

# Sorting the data to see regions with the highest number of registered patients
medical_condition_population=medical_condition_population.sort_values('total_registered_patients',ascending=False)

top_5_regions=medical_condition_population.head()
# The 5 regions with the highest Total Registered Patients are Ealing, Croydon, Barnet, Newham and Brent.
medical_top_5=top_5_regions.boxplot(column=['Hypertension','Obesity (18+)','Diabetes','Asthma','Coronary heart disease'],figsize=(20,10))
medical_top_5.set_xlabel('Medical Conditions')
medical_top_5.set_ylabel('Percentage of registered patients (%)')
plt.title('Medical cases for the 5 regions with the highest number of registered patients')


# Assumption: Adding column to show the most common medical condition within each local authority, i.e. stating which medical condition has the highest number of patients.
# Finding the most common medical condition by local authority.
medical_condition_population['Most common medical condition'] = medical_condition_population[['Hypertension','Obesity (18+)','Diabetes','Asthma','Coronary heart disease']].idxmax(axis=1)
new_df_cases = pd.merge(new_df_cases,medical_condition_population[['Local authority','Most common medical condition']],on='Local authority', how='left')
new_df_cases.head()
# As seen in the boxplot, and further confirmed by the newly added column, Hypertension is the most common medical condition for all local authorities.


# ### 2.1: Reading in the datasets 
# Read columns "country, date, cases" from file "confirmed\_cases\_by\_country.csv" into a dataframe called "cases\_by\_country".
# Read columns "is\_china, date, cases" from "confirmed\_cases\_china\_vs\_world.csv" into a dataframe called "cases\_all". Rename the column "is\_china" to "country" (hint you may use .rename()). Then split this dataframe into two new ones: cases in China ("cases\_china") and cases elsewhere ("cases\_not\_china"). 



cases_by_country=pd.read_csv("confirmed_cases_by_country.csv",usecols=['country','date','cases'])
cases_by_country.head()



cases_all=pd.read_csv("confirmed_cases_china_vs_world.csv",usecols=["is_china","date","cases"])
cases_all = cases_all.rename(columns={'is_china': 'country'})
cases_all.head()



cases_china=cases_all.loc[cases_all['country']=='China'].copy()
cases_not_china=cases_all.drop(cases_china.index[:])
cases_china.head()


# ### 2.2: Summarising the total number of confirmed cases by country 
# Obtain the January records for "cases\_by\_country" and "cases\_china" and summarise cases in China against cases in other countries in a dataframe for this month. Repeat this procedure for February and March. 
# Create a bar plot to compare cases in China with cases in the 5 countries with most cases outside China for January, February and March. 



cases_china['date'] = pd.to_datetime(cases_china['date'])
china=cases_china.copy()
china.insert(0,'month',china['date'].dt.month_name())
china=china.groupby(['month','country'])['cases'].sum().reset_index()
china.head()


cases_by_country['date'] = pd.to_datetime(cases_by_country['date'])
countries=cases_by_country.copy()
countries.insert(0,'month',countries.date.dt.month_name())
countries=countries.groupby(['month','country'])['cases'].sum().reset_index()
countries.head()


# January cases
jan_cases=countries.loc[countries['month']=='January'].sort_values(by='cases',ascending=False)
china_jan= china.loc[china['month'] == 'January']
jan_cases=pd.concat([china_jan,jan_cases])
jan_cases

# February cases
feb_cases=countries.loc[countries['month']=='February'].sort_values(by='cases',ascending=False)
china_feb= china.loc[china['month'] == 'February']
feb_cases=pd.concat([china_feb,feb_cases])
feb_cases

# March cases
mar_cases=countries.loc[countries['month']=='March'].sort_values(by='cases',ascending=False)
china_mar= china.loc[china['month'] == 'March']
mar_cases=pd.concat([china_mar,mar_cases])
mar_cases




# Assumption: Comparing China's cases with 5 countries with most cumulative cases outside China for January to March
countries=countries.groupby(['country'])['cases'].sum().reset_index()
countries.sort_values(by='cases',ascending=False).head()

# The top 5 countries with the highest cumulative cases from Jan to Mar are Italy, Iran, Spain, Germany and South Korea. Creating a list to filter the monthly dataframes for only these countries.
comparing_countries=['China','Italy','Iran','Spain','Germany','Korea, South']
top_5_and_china_jan=jan_cases.loc[jan_cases['country'].isin(comparing_countries)]
top_5_and_china_feb=feb_cases.loc[feb_cases['country'].isin(comparing_countries)]
top_5_and_china_mar=mar_cases.loc[mar_cases['country'].isin(comparing_countries)]
top_5_countries_vs_china=pd.concat([top_5_and_china_jan,top_5_and_china_feb, top_5_and_china_mar],ignore_index=True)

# Structuring data for graphical analysis
top_5_countries_vs_china=top_5_countries_vs_china.set_index(['month','country'])
top_5_countries_vs_china=top_5_countries_vs_china.unstack()

# Arranging the months in order using categorical indexing
top_5_countries_vs_china.index = pd.CategoricalIndex(top_5_countries_vs_china.index, categories=['January','February','March'], ordered=True)
top_5_countries_vs_china = top_5_countries_vs_china.sort_index()
jan_mar_trend=top_5_countries_vs_china.plot.bar(title='3-month trend of cases in China versus 5 countries with most cases outside China',figsize=(20,10))
jan_mar_trend.set_ylabel('Number of Cases')


# ### 2.3: Plotting the accumulated cases by date 
# 
# Add a new column called "acc\_cases" in both  "cases\_not\_china" and "cases\_china" dataframes, which contains the accumulated number of cases by date. Create a time series plot for "acc\_cases" column in "cases\_not\_china" dataframe.



# Case 1 for Assumption 1
# Assumption 1: Accumulated number of cases by date refers to the total number of daily cases.
cases_china['acc_cases'] = cases_china.groupby(['date']).cumsum()
cases_not_china['acc_cases']=cases_not_china.groupby(['date']).cumsum()
accumulated_cases=cases_not_china.plot(x='date',y='acc_cases',title="Accumulated number of cases by date for countries (excluding China)",figsize=(20,10))
accumulated_cases.set_ylabel('Number of Cases')
# This graph makes it easier to spot specific dates where the daily cases spiked.


# Case 2 for Assumption 2
# Assumption 2: Accumulated number of cases by date refers to the cumulative number of daily cases.
cases_not_china['acc_cases']=cases_not_china['cases'].cumsum()
cumulative_cases=cases_not_china.plot(x='date',y='acc_cases',title="Cumulative number of cases by date for all countries (excluding China)",figsize=(20,10))
cumulative_cases.set_ylabel('Number of Cases')
# This graph helps visualise where the rate of infections rise exponentially.


# ### 2.4: Analysing across countries
# When the number of COVID-19 cases became higher than 10,000 in China, what was the number of cases for all other counties in that day? Print the 5 countries with highest number of cases. 


# During the first 5 days that the daily cases in China dropped below 100, what is average number of cases for other countries? Report the top 5 countries with average number of cases.


# Finding the date(s) where daily cases in China were beyond 10,000
more_than_10k_china=cases_china.loc[(cases_china['cases']>10000)]
more_than_10k_china
# China had only one instance between January to March where daily cases exceeded 10,000, which was on the 13th of February 2020, where they had 15,136 new cases.

february13_other_countries=cases_by_country.loc[(cases_by_country['date']=='2020-02-13')]
february13_other_countries=february13_other_countries.groupby(['country']).sum()
february13_other_countries.sort_values('cases',ascending=False).head()
# On the date when China had more than 10,000 cases, Singapore had 8 cases, Vietnam had 1 case, US had 1 case and Malaysia had 1 case.




# Finding the first 5 days that the daily cases in China dropped below 100
less_than_100_china=cases_china.loc[(cases_china['cases']<100)]
less_than_100_china=less_than_100_china['date'].head(5).tolist()
dates_below_100_cases_countries=cases_by_country.loc[cases_by_country['date'].isin(less_than_100_china)]

# Assumption: The average number of cases for other countries is the average number of daily cases on the first 5 dates where China had less than 100 daily cases.
dates_below_100_cases_countries=dates_below_100_cases_countries.groupby(['country'])['cases'].mean().reset_index()
dates_below_100_cases_countries=dates_below_100_cases_countries.sort_values('cases',ascending=False)
top_5_highest_average=dates_below_100_cases_countries['country'].head().tolist()
print("The top 5 countries with the highest average number of cases are {}".format(top_5_highest_average))


