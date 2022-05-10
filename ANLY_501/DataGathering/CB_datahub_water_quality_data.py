#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 09:01:41 2021

@author: mattharding
"""

import requests

# Create function for tracking sediment measurements
def sediment(start, end, project_id, geo_attr, attr_id):
    
    # Base url
    BaseURL="http://data.chesapeakebay.net/api.JSON/LivingResources/TidalBenthic/Sediment/"
    
    #URL arguments
    url = BaseURL+ start+'/'+ end+'/'+'/'+ project_id+'/'+ geo_attr+'/'+attr_id+'/'
   
    #API Response
    response = requests.get(url)
    #print(response.status_code)
    
    # Convert to JSON
    jsontxt = response.json()
    return(jsontxt)


# specific URL information for API
start = "6-29-2010"
end = "6-29-2015"
proj_id = '1' # Tidal Mainstem Water
geo_attr = "Station"
attr_id = '1174' # Main Channel

# Call function for arguments
sed = sediment(start,end,proj_id,geo_attr,attr_id)

# Create CSV file to store data
MyFile = open('Sediment.csv','w')
WriteThis = "Station,Station Description,Date,Source,Value,Sample Type,Depth\n"
MyFile.write(WriteThis)
MyFile.close()

MyFile = open('Sediment.csv','a')
for items in sed:
    station = str(items['Station'])
    stat_des = str(items['StationDescription'])
    date = str(items['SampleDate'])
    source = str(items['Source'])
    val = str(items['ReportedValue'])
    sam_type = str(items['SampleType'])
    depth = str(items['TotalDepth'])

    writethis = station +','+ stat_des +','+ date +','+ source +','+ val +','+ sam_type +','+ depth +'\n'
    
    MyFile.write(writethis)

MyFile.close()


