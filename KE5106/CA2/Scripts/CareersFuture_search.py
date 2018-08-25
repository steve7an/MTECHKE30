#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 07:57:54 2018

@author: iss-user
"""


import argparse, os, time
import urllib3, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from selenium.common.exceptions import NoSuchElementException
import csv

'''
getSalary
getCompany
getJobTitle
get
'''
#job_count = 0

def set_job_number():
    global job_count
    job_count = 1

def getContainers(browser,page):
    dataList = []
    job_nbr = 0
    #page_number = 1
    popup_close = 0
    while True:
        try:
            if popup_close == 0: 
                time.sleep(10)
                popup_close = 1
                link = browser.find_element_by_xpath('//*[@id="snackbar"]/div[1]/div/span')
                link.click()
        except Exception as e:
            print(e)
            pass
            
        for containers in page.find_all('div', {"class": "card-list"}):
            #container = containers[0]
            #print('inside container')
            allJobTitle = containers.find_all('div', {'id' : "job-card-"+str(job_nbr)})
            if len(allJobTitle) == 0:
                return dataList
            for job_title in allJobTitle:
                #print("Starting job number"+str(job_nbr))
                #print(job_title.get('id'))
                jobID = job_title.get('id')
                for companyName in job_title.find_all("p", {"name": "company"}):
                    #print(companyName.text)
                    cName = companyName.text
                for job_t in job_title.find_all("h1", {"name": "job_title"}):
                    #print(job_t.text)
                    titleJob = job_t.text
                    
                salary_s = []
                for salary_s in job_title.find_all('span', {"class": "dib"}):
                    #print(salary_s.text)
                    if salary_s.text:
                        salaryDetail = salary_s.text
                        break
            job_nbr = job_nbr +1
            salDet = salaryDetail.replace('"','').replace(",",'').replace('$','').replace('to',',')
            value1 = [jobID,cName,titleJob,salDet]
            dataList.append(value1)
            
            #job_count = job_count +1
        #if job_nbr>=20:
            #break
        '''page_number = page_number+1
        try:
            #link = page.find_element_by_id(str(page_number))
            link = browser.find_element_by_xpath('//*[@id="search-results"]/div[4]/span[2]')
            link.click()
            print("next page")
        except NoSuchElementException:
            print('Exiting the program')
            break
        '''
            #print(job_title.get("id"))
            #print(soup.prettify(job_title))
            #for companyName in job_title.find_all("div", {"class": "w-100"}):
            #for companyName in containers.find_all("p", {"name": "company"}):
        #r = containers.find_all('div', {"id": "job-card-0"})
        #print(r.text())
                #print(containers.get(id))
                #print(companyName.text)
                
            
            #print(job_title.div.w-100["job_title"])
            #for jobName in job_title.fine_all('div', {"class": "w-100"}):
                #print(jobName)
            #for containers in job_title.find_all('div', {"class": "card relative"}):
        #print(len(containers))
        #print(containers)
        #print(soup.prettify(containers[0]))
        #job = container.find_all('div', {"class": ""})
    return dataList

def writeData(listData,fName):
    with open('/home/iss-user/laxman/python_py/data_extract_pre/job_'+fName+'.txt','a') as file:
        writer = csv.writer(file)
        for row in listData:
            writer.writerow(row)
    return
        
def ViewBot_job(browser,fileName):
    page_seq = 2
    dList = []
    while True:
        #sleep to make sure everything loads
        #add random to look human
        time.sleep(random.uniform(6.9,9.9))
        page = soup(browser.page_source,"html.parser")
        #print(page)
        #getLinks(page)
        print("page_number"+ str(page_seq-1))
        dList = getContainers(browser,page)
        writeData(dList,fileName)
        try:
            link = browser.find_element_by_xpath('//*[@id="search-results"]/div[4]/span['+str(page_seq)+']')
            link.click()
            print("next page")
            page_seq = page_seq + 1
            #page = soup(browser.page_source,"html.parser")
            #close_button = browser.find_element_by_id('joyride-tooltip__close')
            #popup_close = 0
        except NoSuchElementException:
            print('Exiting the program')
            break
        except Exception as e:
            print(e)
            print('Need to exit!'+str(page_seq))
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('search', help='career job search')
    #parser.add_argument('salary', help='career job salary')
    args = parser.parse_args()
    
    browser = webdriver.Chrome()
    browser.get('https://www.mycareersfuture.sg')
    searchString = args.search
    searchElement = browser.find_element_by_id('search-text')
    searchElement.send_keys(args.search)
    #Software Engineer")
        #args.email)
    '''
    if len(args[2]) !=0:
        minSalElement = browser.find_element_by_id('min-salary')
        minSalElement.send_keys(args.salary)
    '''
    searchButton = browser.find_element_by_id('search-button')
    searchButton.click()
            #args.password)
    #minSalElement.submit()
    
    set_job_number()
    os.system('clear')
    print("[+] Success! Logged in, Bot starting")
    ViewBot_job(browser,searchString.replace(" ","_") )
    browser.close()
    
if __name__ == "__main__":
    main()