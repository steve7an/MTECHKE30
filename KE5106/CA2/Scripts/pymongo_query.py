# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 21:27:31 2018

@author: Steve Tan https://github.com/steve7an
"""
from pymongo import MongoClient
import re
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
import requests
from shared_utility import *
import urllib.parse


def query_primary_ssic(db, company):
    ssic = ""
    if company != "":
        try:
            query = {"CompanyName": get_company_alias(company)}
        #    project = {"PrimarySsicCode"}
            cursor = db.industries.find(query)
            for r in cursor:
                return r['PrimarySsicCode']
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
            , type(e).__name__, e)
    return ssic

def query_db(db):
    '''Return the company, pre and post job position after attending master in NUS ISS'''
    query = {
        "$project": {
            "education": "$educations",
            "_id": 0
        }
    }
    unwind = {
        "$unwind": "$educations"
    }
    group = {
        "$group": {
            "_id": "$Url"
        }
    }
    regx = re.compile("master", re.IGNORECASE)
    match = {
        "$match": {
#            '_id': ObjectId('5b78e48b9b9be5486856fad1'),
            "educations.SchoolName": { '$in': ['National University of Singapore', 
                                                'Institute Of System Science',
                                                'NUS', 'ISS']},
            "educations.DegreeName": regx,
            "educations.FieldOfStudy": { "$in": ['Enterprise Business Analytics','Business Analytics', 
                                                'Knowledge Engineering',
                                                'Knowledge Engineering (Data Science & ""Business Analytics)']}
        }
    }
    project = {
       "$project":
        {
          "_id": 1,
          "Url":1,
         "educations.SchoolName" : 1, 
         "educations.DegreeName":1,
         "educations.FieldOfStudy":1,
         "educations.DatesAttendedOrExpectedGraduationStart":1,
         "educations.DatesAttendedOrExpectedGraduationEnd":1,
         "positions.Title":1,
         "positions.CompanyName":1,
         'positions.DatesEmployedStart':1,
         'positions.DatesEmployedEnd':1
        }
  }
    cursor = db.hireu.aggregate([unwind, match, project])

    
    return cursor


def get_pre_post_master_jobs(results):  
    ''' format the result to be generated into a csv format '''
    ''' schoolname,degree,fieldofstudy,studentType,startdate,enddate,pre-company,pre-industry,pre-startdate,pre-postdate,pre-title,post-company,post-industry,post-startdate,post-enddate,post-title'''
    i = 0
    positions = []
    education = []
    csv_row = []
    header = 'url,schoolname,degree,fieldofstudy,studentType,startdate,enddate,pre-title,pre-company,pre-industry,pre-startdate,pre-enddate,post-title,post-company,post-industry,post-startdate,post-enddate,work exp\n'
    csv_row.append(header)
    try:
        db = setupMongoDB()
        
        for row in results:
#            print (i+1)
#            pprint.pprint(row)
#            lines.append(row)
            lines = []
            lines.append(row['Url'])
            education = row['educations']
            positions = row['positions']
            dateSchoolStart = "na"
            dateSchoolEnd = "na"
            # convert all the dates format into date object for comparison
            if 'DatesAttendedOrExpectedGraduationStart' in education.keys():
                dateSchoolStart = cast_str_todate(education['DatesAttendedOrExpectedGraduationStart'])
            else:
                continue
            
            if 'DatesAttendedOrExpectedGraduationEnd' in education.keys():
                dateSchoolEnd = cast_str_todate(education['DatesAttendedOrExpectedGraduationEnd'])
            
            studentType = "full-time"
            if dateSchoolStart and dateSchoolEnd:
                if (dateSchoolEnd - dateSchoolStart).days/365 > 1:
                    studentType = "part-time"
            
            lines.append(clean_text(education['SchoolName']))
            lines.append(clean_text(education['DegreeName']))
            lines.append(clean_text(education['FieldOfStudy']))
            lines.append(studentType)
            lines.append(clean_text(dateSchoolStart.strftime('%Y-%m-%d')))
            lines.append(clean_text(dateSchoolEnd.strftime('%Y-%m-%d')))
            
#            studytype = "Full-Time"
#            schoolduration = dateSchoolEnd - dateSchoolStart
#            if schoolduration > 365:
#                studytype = "Part-Time"
#            print ("{} student".format(studytype))   
    #        print ("School start {} and ended on {}".format(dateSchoolStart,dateSchoolEnd))
#            lines.append("{} Class from {} to {}".format(studytype, dateSchoolStart,dateSchoolEnd))
            pre_title = ""
            pre_company = "na"
            pre_company_ind = ""
            pre_start = "na"
            pre_end = "na"
            post_title = "na"
            post_company = "na"
            post_company_ind = ""
            post_start = "na"
            post_end = "na"
            work_experience = 0
            for pos in positions:
               #skip intern position or work
               if "intern" in pos['Title'].lower():
                    continue
                
               dateEmployedStart = cast_str_todate(pos['DatesEmployedStart'])
               dateEmployedEnd = cast_str_todate(pos['DatesEmployedEnd'],"end")
               work_experience = work_experience + (dateEmployedEnd - dateEmployedStart).days
               print (work_experience)
    #           print ("Position start {} and ended on {}".format(dateEmployedStart,dateEmployedEnd))
               # skip if same start date for position and work
               if dateEmployedStart == dateSchoolStart:
                   continue
               # take the latst position
               if dateEmployedStart <= dateSchoolStart and pre_title == "":
                   pre_title = pos['Title']
                   pre_company = pos['CompanyName']
                   pre_start = dateEmployedStart.strftime('%Y-%m-%d')
                   pre_end = dateEmployedEnd.strftime('%Y-%m-%d')
                   pre_company_ind = query_primary_ssic(db, pre_company)
               # take the earliest position
               if dateEmployedStart >= dateSchoolStart:
                   post_title = pos['Title']
                   post_company = pos['CompanyName']
                   post_start = dateEmployedStart.strftime('%Y-%m-%d')
                   post_end = dateEmployedEnd.strftime('%Y-%m-%d')
                   post_company_ind = query_primary_ssic(db, post_company)
                   
            lines.append(clean_text(pre_title))
            lines.append(clean_text(pre_company))
            lines.append(clean_text(pre_company_ind))
            lines.append(clean_text(pre_start))
            lines.append(clean_text(pre_end))
            
            lines.append(clean_text(post_title))
            lines.append(clean_text(post_company))
            lines.append(clean_text(post_company_ind))
            lines.append(clean_text(post_start))
            lines.append(clean_text(post_end))
            lines.append(str(format_to_year(work_experience)))
            tmp_line = ",".join(lines)
            csv_row.append(tmp_line+ "\n")
#            print ("{}:{}\n\n".format(i,tmp_line))
            
            i = i + 1
        print ("Total matches: {}".format(i))
    except Exception as e:
        print('Error on line {} for row {}'.format(sys.exc_info()[-1].tb_lineno, row)
            , type(e).__name__, e)
        #b_exception = 1
        
    return (csv_row)


    
def get_industry_info_by_company(company):
    '''Given company name retrieve the SSIC, SSIC description, issuance agency, address, company type, entity type '''
    url = 'https://opencorpdata.com/sg?q={}'.format(urllib.parse.quote_plus(company))
#    print (url)
    page = requests.get(url)
    soup = ""
    if page.status_code == 200:
        tmp_hash = {}
        infos = []
        try:
            soup = BeautifulSoup(page.text, 'html.parser')
#            return soup
        
            #get the first link, assume it's correct
            links = soup.find_all('div', class_='panel-body')[-1].find_all("a")
            company_url = ""
            for link in links:
#                print (clean_text(link.get_text()))
                if company_url=="": # and clean_text(link.get_text()).startswith(company.upper() +" "):
#                    print (link['href'])
                    company_url = link['href']
            
            #follow the link
            page = requests.get(company_url)
            soup = BeautifulSoup(page.text, 'html.parser')
            # get all the company info
            tds = soup.find('div',id='overview').find_all("td")
            for td in tds:
                infos.append(clean_text(td.get_text()))
            for i in range(0,len(infos),2):
                tmp_hash[infos[i].title().replace(" ","").replace(".","")] = clean_text(infos[i+1])
    
        except Exception as e:
            print('Error on line {} for url {}'.format(sys.exc_info()[-1].tb_lineno, url)
                , type(e).__name__, e)
    return tmp_hash

def get_unique_companies(lines):
    ''' process the csv format data and retrieve a list of unique company names '''
    dict_companies = {}
    for i, line in enumerate(lines):
        if i == 0:
            continue
        
        precompany = line.split(",")[7]
        if precompany not in dict_companies.keys():
            dict_companies[precompany] = 1
        postcompany = line.split(",")[11]
        if postcompany not in dict_companies.keys():
            dict_companies[postcompany] = 1
            
    return dict_companies

def get_industry_infos(companies):
    ''' 
    Given companies, query for the industry info 
    Also return the companies which we weren't able to match
    '''
    industries = []
    error_list = []
    for c in companies:
        alias = get_company_alias(c)
        if alias != '':
            c = alias
        
        print ("Fetching industry information for {}".format(c))
        industry = get_industry_info_by_company(c)
        print ("Industry for {}".format(industry))
        if 'EntityName' in industry.keys()\
            and industry['EntityName'].lower().startswith(c.split()[0].lower()):
            industry['CompanyName'] = c
            industries.append(industry)
        else:
            error_list.append(c)

    return (industries, error_list)



def create_industries_collection(db, industries):
    ''' create industries collection '''
    db.industries.delete_many({})

    #insert into hireu table
    db.industries.insert_many(industries)

def get_company_alias(company):
    ''' return SSIC compliant company name if available '''
    
    dict_alias = { 'KPMG':'KPMG LLP',
     'HP':'HEWLETT PACKARD ENTERPRISE',
     'Bank of America Merrill Lynch':'',
     'EY':'Ernst & Young LLP',
     'Turck Banner Singapore Pte Ltd':'Turck Banner Singapore',
     'na':'',
     'Singapore Armed Forces':'',
     'Defence Science & Technology Agency':'',
     'KPMG Singapore':'KPMG LLP',
     'Rolta India Limited':'',
     "ACP Computer Training School Pte' Ltd'":'ACP COMPUTER TRAINING SCHOOL',
     'Xtremax Pte Ltd':'XTREMAX',
     "www'forthepeople'net'in":'',
     'Decision Solutions Pte Ltd':'DECISION SOLUTIONS',
     'PhilipsElectronics SIngapore Pte Ltd':'PHILIPS ELECTRONICS',
     "Dr' Reddy's Laboratories":'DR REDDYS',
     "Vuclip Inc'":'VUCLIP (SINGAPORE)',
     'Middle Kingdom Group':'',
     'National University of Singapore':'',
     'Analytics Quotient':'',
     'NUS Business School':'',
     "MindTree Ltd'":'MINDTREE LIMITED (SINGAPORE BRANCH)	',
     'Centre for Maritime Studies NUS':'',
     'AXA SEA':'AXA HEALTHCARE',
     'Sense Infosys Pte Ltd':'SENSE INFOSYS',
     'IBM Global Business Services':'IBM GLOBAL SERVICES',
     'Singapore University of Social Sciences':'SINGAPORE UNIVERSITY OF SOCIAL SCIENCES',
     'Lenovo-Global Analytics Hub':'LENOVO (SINGAPORE)',
     'Micron Technology':'MICRON TECH',
     'CrossTrack Pte Ltd':'CROSSTRACK',
     'Wipro Technologies':'WIPRO SINGAPORE',
     'CrimsonLogic Defense Science Organisation(DSO) Singapore':'CRIMSONLOGIC',
     'Bluefish Technologies Group':'BLUEFISH TECHNOLOGIES',
     "iDirect Asia Pte' Ltd'":'IDIRECT ASIA',
     'Deepdive Solutions Pvt Ltd':'',
     'NCS Group':'NCSOLUTIONS',
     'Keppel FELS Ltd':'KEPPEL TECHNOLOGY AND INNOVATION',
     'GovTech Singapore':'',
     "Combuilder Pte' Ltd'":'COMBUILDER ENGINEERING',
     'A*STAR - Agency for Science Technology and Research':'A*STAR RESEARCH ENTITIES',
     'Republic of Singapore Navy':'Republic of Singapore Navy',
     "iCognitive Pte' Ltd' Singapore":'ICOGNITIVE',
     'ST Electronics (Info-Software Systems) Pte Ltd':'ST ELECTRONICS',
     'Great Eastern Life':'THE GREAT EASTERN LIFE ASSURANCE',
     "Etiqa Insurance Pte' Ltd'":'ETIQA INSURANCE',
     'PSA Corporation Limited':'PSA CORPORATION LIMITED',
     'Vassar Labs':'',
     'Resorts World Sentosa':'RESORTS WORLD (SINGAPORE)',
     'SMRT Corporation Ltd':'SMRT CORPORATION LTD',
     'Ernst and Young (EYC3)':'Ernst & Young LLP',
     'Lee Kuan Yew School of Public Policy':'',
     'Medix Multimedia Consultancy Pte Ltd':'MEDIX TECHNOLOGIES',
     'Singapore Computer Systems Limited':'SINGAPORE COMPUTERS',
     "Cognitive ECM Pte' Ltd'":'COGNITIVE ECM',
     'Islamic Religious Council of Singapore (MUIS)':'Persatuan Ulama dan Guru-Guru Agama Islam',
     'Motor Corporation':'',
     'Inkriti':'',
     "OBS Financial Solutions Pte' Ltd'":'OBS FINANCIAL',
     'Land Transport Authority (LTA) Singapore':'Land Transport Authority of Singapore',
     "SINGHOST'NET":'SINGHOST',
     'Sompo International':'SOMPO HOLDINGS',
     'ANZ':'ANZ INTERNATIONAL PRIVATE BANKING',
     'Samtel Avionics':'',
     'RBEI':'ROBERT BOSCH',
     'GIC':'GIC (INTERNATIONAL)',
     "ST Electronics (Info-Software Systems) Pte' Ltd'":'ST ELECTRONICS',
     'Temasek':'TEMASEK HOLDINGS',
     "J'D' Power and Associates":'J.D. POWER',
     'Barclays Technology Centre Singapore':'BARCLAYS CAPITAL HOLDINGS',
     'IHiS (Integrated Health Information Systems)':'INTEGRATED HEALTH INFORMATION SYSTEMS',
     'AI Singapore':'',
     'MIMS Pte Ltd':'MIMS',
     'NVPC - National Volunteer & Philanthropy Centre':'NATIONAL VOLUNTEER AND PHILANTHROPY CENTRE',
     'Ministry of Defence of Singapore':'',
     'Renesas Electronics Corporation':'RENESAS ELECTRONICS',
     'Ecquaria Technologies Pte Ltd':'',
     'IBM International Holdings Singapore':'IBM INTERNATIONAL',
     'Paladion Networks':''}

    if company in dict_alias.keys():
        company = dict_alias[company]

    return company

#cwd = os.getcwd()
#file_path  = r'{}\results{}.txt'.format(cwd,get_timestamp())
#sys.stdout = open(file_path, 'w', encoding="utf-8")
db = setupMongoDB()
    
results = query_db(db)
lines = get_pre_post_master_jobs(results)
write_results_to_csv(lines)
#comps = get_unique_companies(lines)

#probs = ['Bank of America Merrill Lynch',
# 'Defence Science & Technology Agency',
# 'Rolta India Limited',
# "www'forthepeople'net'in",
# 'Middle Kingdom Group',
# 'Analytics Quotient',
# 'Deepdive Solutions Pvt Ltd',
# 'GovTech Singapore',
# 'A*STAR RESEARCH ENTITIES',
# 'Vassar Labs',
# 'Inkriti',
# 'Samtel Avionics',
# 'GIC (INTERNATIONAL)',
# 'J.D. POWER',
# 'Uber',
# 'AI Singapore',
# 'Ministry of Defence of Singapore',
# 'Paladion Networks']
#industries,errors = get_industry_infos(remove_duplicates_from_list(probs))

#industries,errors = get_industry_infos(list(comps.keys()))
#
#db = setupMongoDB()
#create_industries_collection(db, industries)
    
#for l in lines:
#    pprint.pprint(l)
#export_query_results(lines)
#export_query_results(results)

#industry = get_industry_info_by_company('KPMG LLP')
#print (industry)
#print (soup.find_all('div', class_='panel-body')[-1].find("a")["href"])

#db = setupMongoDB()
#ssic = query_primary_ssic(db, 'EY')
#print (ssic)
#for c in ssic:
#    print (c['PrimarySsicCode'])