# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 18:49:07 2018

@author: Steve Tan https://github.com/steve7an
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

import os
import time
import math

import sys, os

from shared_utility import *


def login():
    ''' Disable the 2fa so that we can automate the login, otherwise LinkedIn doesnt work '''
    userid = str(input("Enter email address: "))
    password = getpass.getpass('Enter your password:')
    
    
    driver.get("https://www.linkedin.com")
    driver.implicitly_wait(imp_delay)
    driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
    driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
    driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()


def get_profile(connection_url):
    ''' Given a profile link, get the needed details and return them as an dict'''
    profile = {}
    driver.get(connection_url)
    driver.implicitly_wait(imp_delay)
    
    scroll_smooth(driver)
    scroll_smooth(driver,"up")
    b_exception = 0
    try:
        classname = 'experience-section'
        myElem = WebDriverWait(driver, exp_delay).until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        if debug_mode:
            print (classname + " loading is ready!")
    except Exception as e:
        #print ("{}: error {} loading took too much time!".format(classname, e))
        print('Error on line {} for section {} for url {}'.format(sys.exc_info()[-1].tb_lineno, classname, connection_url)
        , type(e).__name__, e)
        b_exception= 1

        
    try:
        classname = 'education-section'
        myElem = WebDriverWait(driver, exp_delay).until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        if debug_mode:
            print (classname + " loading is ready!")
    except Exception as e:
        #print ("{}: error {} loading took too much time!".format(classname, e))
        print('Error on line {} for section {} for url {}'.format(sys.exc_info()[-1].tb_lineno, classname,connection_url)
        , type(e).__name__, e)
        b_exception= 1


    html=driver.page_source   
    soup=BeautifulSoup(html, "lxml") #specify parser or it will auto-select for you
    #return soup
   
    name = soup.find("h1", class_="pv-top-card-section__name").get_text().strip()
    title = soup.find("h2", class_="pv-top-card-section__headline").get_text().strip()
    location = soup.find("h3", class_="pv-top-card-section__location").get_text().strip()
    
    positions = []
    tmp = []
    try:
        i = 1
        exps = soup.find("section", class_="experience-section").find_all("li", class_="pv-position-entity")
        for exp in exps:
            tmp = [s for s in exp.find("div",class_="pv-entity__summary-info").get_text().splitlines() if s.strip()]
            
            tmp_hash = {}
            if len(tmp) == 1:
                positions.append({"Title":tmp[0].strip()})
            elif len(tmp) % 2 == 1: # having odd no of elements
                tmp_hash["Title"] = tmp[0].strip()

                for j in range(1,len(tmp),2):
                    # add handling for dates field
                    if "dates" in tmp[j].lower():
                        tmp_hash[tmp[j].title().replace(" ","") + "Start"] = tmp[j+1].split("–")[0].strip()
                        tmp_hash[tmp[j].title().replace(" ","") + "End"] = tmp[j+1].split("–")[1].strip()
                    else:
                        tmp_hash[tmp[j].title().replace(" ","").replace(".","")] = clean_text(tmp[j+1])
                positions.append(tmp_hash)
            else:
                print ("Unrecognised format for experience section found for url {}".format(connection_url))
            i = i + 1
    except Exception as e:
        #print ("Experience section for {} encountered error {}".format())
        print('Error on line {} for url {}'.format(sys.exc_info()[-1].tb_lineno, connection_url)
        , type(e).__name__, e)
        b_exception = 1

    educations = []
    try:
        i = 1
        edus = soup.find("section", class_="education-section").find_all("div", class_="pv-entity__summary-info")
        for edu in edus:
            tmp = [s for s in edu.get_text().splitlines() if s.strip()]
            if len(tmp) == 1:
                educations.append({"SchoolName":tmp[0].strip()})
            elif len(tmp) % 2 == 1: # having odd no of elements
                tmp_hash = {}
                tmp_hash["SchoolName"] = tmp[0]
                for j in range(1,len(tmp),2):
                    # add handling for dates field
                    if "dates" in tmp[j].lower():
                        tmp_hash[tmp[j].title().replace(" ","") + "Start"] = tmp[j+1].split("–")[0].strip()
                        tmp_hash[tmp[j].title().replace(" ","") + "End"] = tmp[j+1].split("–")[1].strip()
                    else:
                        tmp_hash[tmp[j].title().replace(" ","").replace(".","")] = clean_text(tmp[j+1])
                educations.append(tmp_hash)
            else:
                print ("Unrecognised format for education section found for url {}".format(connection_url))
            i = i + 1
    except Exception as e:
#        print ("Education section for url {} encountered error {}".format(connection_url, e))
        print('Error on line {} for url {}'.format(sys.exc_info()[-1].tb_lineno, connection_url)
        , type(e).__name__, e)
        b_exception = 1
        
    # recapture the profile later if an exception is found
    if not (b_exception):
        profile['name'] = name
        profile['title'] = title
        profile['location'] = location
        profile['Url'] = connection_url
        profile['positions'] = positions
        profile['educations'] = educations

    
    return (profile)
    
    #mydivs = soup.findAll("div", {"class": "pv-top-card-v2-section__info"})
    #return (mydivs)


def test_get_profiles():
    connection_urls = ['https://www.linkedin.com/in/laxman-singh-pmp-6304a622/', 'https://www.linkedin.com/in/jelina-cheng-69b12a61/']
    profiles = []
    for url in connection_urls:
        profiles.append(get_profile(url))
        
def setup_driver():
    cwd = os.getcwd()
    firefox_path = r'{}\geckodriver.exe'.format(cwd)
    #driver = webdriver.Firefox(executable_path=firefox_path)
    #driver.set_page_load_timeout(30)

    chrome_path=r'{}\chromedriver.exe'.format(cwd)    
    #option = webdriver.ChromeOptions()
    #option.add_argument(" — incognito")
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
    driver = webdriver.Chrome(chrome_path, chrome_options=opts)
    return driver         


        
def scroll_around(driver):
    '''Move around the page so that the links will load properly'''
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(get_sleep_delay())
    if debug_mode:
        print ("3: {}".format(len(driver.page_source)))

    driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight/2);")
    time.sleep(get_sleep_delay())
    if debug_mode:
        print ("5: {}".format(len(driver.page_source)))
    
    driver.execute_script("window.scrollTo(document.body.scrollHeight/2, 0);")
    time.sleep(get_sleep_delay())
    if debug_mode:
        print ("6: {}".format(len(driver.page_source)))
    
def scroll_smooth(driver, direction="down"):
    steps = 900
    if direction=="down":
        for i in range(1, steps+1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight* ({}/{}));".format(i, steps))
    else:
        for i in range(1, steps+1):
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight* ({}/{}));".format(steps-i, steps))
    time.sleep(get_sleep_delay())
    if debug_mode:
        print ("7: {}".format(len(driver.page_source)))


def get_profile_links(soup):
    links = []
    profiles = soup.find_all("div",class_='search-result__info')
    for p in profiles:
        href_txt = p.find("a",href=True)['href']
        if len(href_txt) > 1:
            url = "https://www.linkedin.com{}".format(href_txt)
            links.append(url)
        else:
            print ("Unmatch url {}".format(href_txt))
    return links

def get_links(search_url):
    profile_links = []
    driver.implicitly_wait(imp_delay)
    driver.get(search_url)
#    time.sleep(get_sleep_delay())
    
    if debug_mode:
        print ("1: {}".format(len(driver.page_source)))

    scroll_smooth(driver)
#    scroll_smooth(driver, "up")
    html=driver.page_source
    soup=BeautifulSoup(html, "lxml") #specify parser or it will auto-select for you
    #return soup

    '''Given a search linkedin Url, retrieve all the profiles link'''
    #get each profile link in the page and add them to the array
    #search-result__info
    tmp = get_profile_links(soup)
    profile_links.extend(tmp)
    print ("Fetching {} profiles".format(len(tmp)))

    #get the paging links and loop through each one
    padding = 1 # for the last page 
    total_pages = math.ceil(int(soup.find('h3',class_='search-results__total').get_text().replace(",","").split()[1])/10) + padding
    
    #bounded to linkedin 100 pages
    if total_pages > 100:
        total_pages = 101
        
    for i in range(2,total_pages):
        driver.implicitly_wait(imp_delay) # seconds
        driver.get(search_url + "page&page={}".format(i))
#        time.sleep(get_sleep_delay())
        
        scroll_smooth(driver)
#        scroll_smooth(driver, "up")

        html=driver.page_source
        soup=BeautifulSoup(html, "lxml") #specify parser or it will auto-select for you
        tmp = get_profile_links(soup)
        profile_links.extend(tmp)
        print ("Fetching {} profiles".format(len(tmp)))
    
        print("Processing page {} out of total page {}".format(i, total_pages))
    #return the array
    return profile_links

def create_profiles_collection(db, profiles):
    # Ensure everything is deleted from example collection.
    # ... The name can anything to specify a collection.
    #db.hireu.delete_many({})
    
    #insert into hireu table
    db.hireu.insert_many(profiles)
    
    # Find all things.
#    cursor = db.hireu.find({})
#    print("FIND ALL")
#    for c in cursor:
#        print(c)

def get_new_links_only(db, links):
    ''' check against mongodb to return only the new links '''
    result = db.hireu.find({ "Url" : { "$in": links}})
    try:
        url = ""
        for doc in result:
            url = doc['Url']
            links.remove(url)
    except Exception as e:
        print('Error on line {} for url {}'.format(sys.exc_info()[-1].tb_lineno, url)
        , type(e).__name__, e)
    
    return links

random.seed(1098)
debug_mode = 0
#sleep_delay = 1
exp_delay = 60 #60 secs is sufficient?
imp_delay = 3
driver = setup_driver()
login()

#search_url = 'https://www.linkedin.com/search/results/index/?keywords=nus%20iss%20master%20tech&origin=GLOBAL_SEARCH_HEADER'

# NUS ISS grads only?
#search_url = "https://www.linkedin.com/search/results/index/?keywords=%22National%20University%20of%20Singapore%22%20or%20%22NUS%22%20or%20%22Institute%20of%20System%20Science%22%20or%20Master&origin=GLOBAL_SEARCH_HEADER"

# current set of links - not very accurate for KE students
#search_url = "https://www.linkedin.com/search/results/index/?keywords=Institute%20System%20Science%20NUS&origin=GLOBAL_SEARCH_HEADER"

# trying KE only links
#search_url = "https://www.linkedin.com/search/results/index/?keywords=master%20of%20technology%20knowledge%20engineering%20National%20University%20of%20Singapore&origin=GLOBAL_SEARCH_HEADER"

# getting EBAC only links
search_url = "https://www.linkedin.com/search/results/index/?keywords=master%20of%20technology%20business%20analytics%20National%20University%20of%20Singapore&origin=GLOBAL_SEARCH_HEADER"
links = get_links(search_url)
write_links_to_file(links)

#links = ['https://www.linkedin.com/in/vandana-vamadevan-pillai-121b8774/','https://www.linkedin.com/in/wei-gang-40b3647/',
#         'https://www.linkedin.com/in/nickguan/','https://www.linkedin.com/in/toon-seng-foo-2726701a/']

#links = ['https://www.linkedin.com/in/meiyou-ye-9643075/'
#,'https://www.linkedin.com/in/siong-guan-ang-a6a759a6/'
#,'https://www.linkedin.com/in/zheming-chen-3b667064/'
#,'https://www.linkedin.com/in/jianlin-luo-33236735/'
#,'https://www.linkedin.com/in/lamboonsoon/'
#,'https://www.linkedin.com/in/wilsonwan/']
#reload from links file to continue
#db = setupMongoDB()
#cwd = os.getcwd()
#links_file = '{}\data\links20180823124257.txt'.format(cwd)
#links = read_links_from_file(links_file)

unique_links = get_new_links_only(db, links)
print (len(unique_links))
#
total_links = len(unique_links)
profiles = []
for i, url in enumerate(unique_links):
    print ("processing {} out of {} links.".format(i + 1, total_links))
    profiles.append(get_profile(url))
    
#driver.quit()
#
##
#cwd = os.getcwd()
#file_path  = '{}\data\data_formatted{}.json'.format(cwd,get_timestamp())
#export_profiles_as_json(file_path, profiles)
##profiles = load_profiles_from_json(file_path)
#
create_profiles_collection(db, profiles)

#query_db()
#
#write_links_to_file(links)


#one = [1,2,3]
#two = [4,5,6]
#one.extend(two)
#print (one)