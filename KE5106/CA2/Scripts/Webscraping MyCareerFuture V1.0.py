
# In[1]:
"""
Created on Wed Aug 15 14:30:24 2018

@author: Muthuraman Ramasamy
"""
import requests
import bs4
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import urllib.request

# In[6]:

# set URL https://www.mycareersfuture.sg/search?search=Data%20scientist&page=0
url_template = "https://www.mycareersfuture.sg/search?search=Data%20scientist&page={}"
# Set this to a high-value to generate more results. 
max_results_per_city = 4 
#Data frame structure
df = pd.DataFrame(columns=["location", 'company', 'job_title', 'salary_low','salary_high', 'Days Old'])
cities = ['Singapore']
for city in cities:
    print (city)
    for start1 in range(0, max_results_per_city, 1):
        print (start1)
        url = url_template.format(start1)
        print (url)
        with urllib.request.urlopen(url) as response:
         html = response.read()
         soups = BeautifulSoup(html, "html.parser")
         for b in soups.find_all('div', attrs = {'class':'card-list'}):
                    #location = b.find('span', attrs = {'class': 'location'}).text
                    location = "Singapore"
                    print ("in loooooop")
                   # job_title = b.find('a', attrs = {'data-tn-element':'jobTitle'}).text
                    try:
                        job_title = b.find('job_title', attrs = {'class':'f4-5 fw6 mv0 brand-sec dib mr2 JobCard__jobtitle___3HqOw'}).text
                    except:
                        job_title = 'NA' 
                    try:
                        company = b.find('company', attrs = {'class':'f6 fw6 mv0 black-80 mr2 di ttu'}).text
                    except:
                        company = 'NA'
                    print ("Company", company)
                    try:
                        salary_low = b.find('span', attrs = {'class' : 'dib'}).text  
                    except:
                        salary_low = 'NA'
                    try:
                        salary_high = b.find('span', attrs = {'class' : 'f5 fw4 ph1'}).text  
                    except:
                        salary_high = 'NA'
                    try:
                        Days_old = b.find('last_posted_date', attrs = {'class':'gray mv0 f6 fw4 i'}).text
                    except:
                        Days_old = '0'

                    salary = salary.strip('\n $')
                    salary = salary.strip(' $')
                    salary = salary.strip('a month')
                    Days_old = Days_old.strip('ago')
                    df = df.append({"location":location,"company":company, "job_title": job_title, "salary_low": salary_low,"salary_high": salary_high, "Days Old":Days_old }, ignore_index=True) 
print ("Scraping Completed successfully")        
df.head()

# In[7]:


#sending it to csvs to save the data
df.to_csv("~/Desktop/Career_future_Jobs_Data.csv" , sep=',', encoding='utf-8')


df1 = pd.read_csv('~/Desktop/Career_future_Jobs_Data.csv')



# In[9]:

data = pd.concat([df1]) #making into one df
data.drop(['Unnamed: 0'], axis=1, inplace=True) #resetting index
data.drop_duplicates(inplace=True) #dropping duplicates

# In[10]:


def eda(dataframe): #code chunk to check quality of data
    print ("missing values \n", dataframe.isnull().sum()) #shows total amount of null values for each column
    print ("dataframe types \n", dataframe.dtypes)
    print ("dataframe shape \n", dataframe.shape)   
    print ("dataframe describe \n", dataframe.describe())
    print ("dataframe length =", len(dataframe)) #length of the dataframe
    print ("duplicates", dataframe.duplicated().sum()) # added this to duplicates in the data
    for item in dataframe:
        print (item)
        print (dataframe[item].nunique())
eda(data)

