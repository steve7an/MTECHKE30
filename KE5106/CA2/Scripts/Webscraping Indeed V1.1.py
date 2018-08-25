
# In[1]:
import requests
import bs4
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import urllib.request

# In[6]:
# q = ['Data+Analyst','Data+Scientist','Project+Manager','Consultant','Software+Engineer','Senior+Software+Engineer','Research+Assistant','Product+Developer+(Analytics)','Ad+Hoc+Trainer','Senior+System+Analyst','Consulting+Manager','Business+Analytics+Developer','Contract+Predictive+Analyst','Senior+Manager+/+Architect','Data+&+Analytics+-+Senior+Consultant','Strategic+Policy+&+Planning+Manager','Assistant+Manager','Member+of+Technical+Staff+(MTS)+-+IT','Data+Analyst+-+Pricing+Analytics','Principal+Analyst+(Data+Analytics)','Data+Analyst+(consumer+analysis+part-time)','Apprentice','Data+Migration+Manager','Business+Analyst','Data+Quality+Consultant','Business+Analytics+Analyst','Data+Science+(Data+Innovation+Lab)','Web+Hosting+Manager','Data+Science+Analyst','IT+Consultant','Associate','MTS+(Member+of+Technical+Staff)+YMS','Asst+Principal+Engineer','Operations+Planning+Analyst','Senior+Actuary+Actuarial+and+Risk+Management','Principal+Consultant','Senior+Associate','Product+Support+Engineer','Senior+Consultant','Senior+Data+Architect','Data+Scientist+-+Advanced+Analytics','Senior+Analyst','Deputy+Head+of+Department','Senior+Business+Analyst','Development+Manager','Senior+Data+Analyst','Director+Global+Research+Services','Senior+Engineer','Senior+Security+Engineer','Enterprise+Data+Architect|Enterprise+Architect+Office','Senior+Statistical+Analyst','Entrepreneur','Senior+Systems+Engineer','Executive','Sr'+Project+Manager+(SkillsFuture+Singapore)','Functional+Consultant','Vice+President+IT','Global+Data+Analyst','Workflow+and+BPM+Product+Manager','Graduate+Research+Assistant','IT+Analyst']
q1 = ['Data+Analyst','Data+Scientist','Project+Manager']

# set URL
url_template = "https://www.indeed.com.sg/jobs?q={}&l=Singapore&start={}"
# Set this to a high-value to generate more results. 
max_results_per_city = 1000
#Data frame structure
df = pd.DataFrame(columns=["location", 'company', 'job_title', 'salary', 'Days Old'])
cities = ['Singapore']
for q in q1:
    print (q)
    for start1 in range(0, max_results_per_city, 10):
        print (start1)
        url = url_template.format(q,start1)
        print (url)
        with urllib.request.urlopen(url) as response:
         html = response.read()
         soups = BeautifulSoup(html, "html.parser")
         for b in soups.find_all('div', attrs = {'class':' row result'}):
                    location = b.find('span', attrs = {'class': 'location'}).text
                    job_title = b.find('a', attrs = {'data-tn-element':'jobTitle'}).text
                    try:
                        company = b.find('span', attrs = {'class':'company'}).text
                    except:
                        company = 'NA'
                    try:
                        salary = b.find('span', attrs = {'class' : 'no-wrap'}).text  
                    except:
                        salary = 'NA'
                    try:
                        Days_old = b.find('span', attrs = {'class':'date'}).text
                    except:
                        Days_old = '0'
                    company = company.strip('\n')
                    #print (company)
                    salary = salary.strip('\n $')
                    salary = salary.strip(' $')
                    salary = salary.strip('a month')
                    Days_old = Days_old.strip('ago')
                    df = df.append({"location":location,"company":company, "job_title": job_title, "salary": salary, "Days Old":Days_old }, ignore_index=True) 
           
df.head()        

# In[7]:


#sending it to csvs to save the data
df.to_csv("~/Desktop/Jobs.csv" , sep=',', encoding='utf-8')


df1 = pd.read_csv('~/Desktop/Jobs.csv')



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

