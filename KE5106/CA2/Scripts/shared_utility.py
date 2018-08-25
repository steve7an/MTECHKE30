# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 20:50:20 2018

@author: Steve Tan https://github.com/steve7an
"""
import json
import datetime, time
from time import strptime
import pprint
import html
import random
import re
import os, sys
from pymongo import MongoClient
from collections import OrderedDict


def get_timestamp():
    import datetime
    return (datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))

def export_query_results(results):
    cwd = os.getcwd()
    file_path  = '{}\query_results{}.txt'.format(cwd,get_timestamp())
    f = open(file_path, "w", encoding="utf-8")
    for r in results:
        f.write(r + "\n")
        
def cast_str_todate(strdate, datetype="start"):
    dateobj = datetime.date.today()
    
    defaultday = 1
    defaultmonth = 1
    if datetype!="start":
        defaultmonth = 12
        
    if strdate != "Present":
        tmp_array = strdate.split(" ")
        #print (tmp_array)
        if len(tmp_array) > 1:
            dateobj = datetime.date(int(tmp_array[1]),
                                strptime(tmp_array[0],'%b').tm_mon, defaultday)
#            print (dateobj)
        else:
            dateobj = datetime.date(int(tmp_array[0]), defaultmonth, defaultday)
#            print (dateobj)

    return dateobj

def clean_text(txt):
    return txt.replace("“","").strip().replace("”","").replace(".","").replace("\"","").replace(",","")

        
def write_results_to_csv(links):
    cwd = os.getcwd()
    file_path  = '{}\lines{}.csv'.format(cwd,get_timestamp())
    f = open(file_path, "w", encoding="utf-8")
    for l in links:
        f.write(l)
    f.close()

def export_profiles_as_json(file_path, profiles):
    ''' Export profiles as json file '''
    with open(file_path, 'w') as outfile:
        json.dump(profiles, outfile)
    
def export_profiles_as_file(file_path, profiles):
    ''' Export profiles as txt file '''
    import sys
    sys.stdout = open(file_path, 'w')
    print (profiles)
    
def load_profiles_from_json(file_path):
    ''' Load profiles from json file '''
    with open(file_path) as f:
        profiles = json.load(f)
    
    return profiles

def write_links_to_file(links):
    cwd = os.getcwd()
    file_path  = '{}\data\links{}.txt'.format(cwd,get_timestamp())
    f = open(file_path, "w")
    for l in links:
        f.write(l + "\n")
    

def read_links_from_file(file_path):
    links = []
    with open(file_path) as file:
        for line in file: 
            links.append(line.strip())
    return links

def get_timestamp():
    import datetime
    return (datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))

def get_sleep_delay():
    return random.randint(1,3)

def setupMongoDB():
    client = MongoClient("mongodb://127.0.0.1:27017")
    # Specify the database name after the client object.
    db = client.hireu

    return db

def remove_duplicates_from_list(items):
    list(OrderedDict.fromkeys(items))
    return list(set(items))

def format_to_year(days):
    years = int(round(days / 365, 0))
    return years
    
    return "{} {} {} {}".format(years, txt_yr, months, txt_mo)

def format_to_year_and_months(days):
    years = int(round(days / 365, 0))
    months = int(round((days % 365)/30, 0))
    txt_yr = "yr"
    if years > 1:
        txt_yr = "yrs"
    txt_mo = "mo"
    if months > 1:
        txt_mo = "mos"
    
    return "{} {} {} {}".format(years, txt_yr, months, txt_mo)

#days = 365
#print (format_to_year_and_months(days))
#months = round((days % 365)/30)