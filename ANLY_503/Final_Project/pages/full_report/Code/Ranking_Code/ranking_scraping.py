#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 16:20:33 2022

@author: mattyoung
"""
##Import libraries
import urllib
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import requests

##Instantiate Web Scraping
def make_soup(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req)
    main_doc = webpage.read()
    return main_doc

################
# This process was a bit more manual than intended. The paths for each NCAA Championship had no clear order.
# Therefore, I hovered on the link to each championship and copied the path of the different years into the xc list below.
####################

xc = ['11762', '11763','10446','10447','9270','9356','5962','5963','5946','5957','5471','5474','5003','5000','4514','4510','4095','4100','3674','3680','3330','3329']
#Create blank list
df_list=[]
for i in xc:
    #Base URL
    url = "https://www.ustfccca.org/team-rankings-polls-central/polls-rankings-hub?coll="+str(i)+"/"
    #Blank collection list
    df_collection=[]
    soup = make_soup(url)
    df_collection.append(pd.read_html(soup))
    #Select only column with ranking data
    df = df_collection[0]
    #Same as above
    df = df[0]
    #Try other method to get text content
    req = requests.get(url)
    content=req.text
    soup2 = BeautifulSoup(content)
    year = soup2.h4.text
    detail = year[5:]
    year = year[0:4]
    season_gender = soup2.find_all("h5")[0].text
    #Season to be extra careful to make sure that information is not from the wrong season/sport
    if 'Cross' in season_gender:
        season = 'Cross Country'
    elif 'Outdoor' in season_gender:
        season = 'Outdoor Track'
    else:
        season = 'Indoor Track'
    if 'III' in season_gender:
        division = 'III'
    elif 'II' in season_gender:
        division = 'II'
    elif 'NJCAA' in season_gender:
        division = 'NJCAA'
    elif 'NAIA' in season_gender:
        division = 'NAIA'
    else:
        division = 'I'
    if 'Women' in season_gender:
        gender = 'Women'
    else:
        gender = 'Men'
    #label all columns with year given
    df['Year'] = year
    #label all columns with season given
    df['Season'] = season
    #label all columns with gender given
    df['Gender'] = gender
    #label all columns with division given
    df['Division'] = division
    #label all columns with date/detail given
    df['Description'] = detail
    df_list.append(df)

#Combine all dataframes into one list
xc_df = pd.concat(df_list)
#Rename columns for understanding
xc_df.rename(columns = {'RANK':'Rank','Unnamed: 1':'Delete','TEAMCONFERENCE':'Team','Unnamed: 3':'Points','Unnamed: 5':'Change','Last Year':'Conference'}, inplace=True)
#Delete blank column
xc_df = xc_df.drop(columns={'Delete'})
#Write to csv
xc_df.to_csv('Data/Ranking_Data/xc_rank.csv', index=False)

