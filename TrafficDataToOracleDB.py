# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 17:52:48 2019

@author: MystakidisAristeis
"""


import urllib.request, json 
import cx_Oracle
import os, json
import pandas as pd
from glob import glob
import time
from datetime import datetime, timedelta

 

def JsonToOracle():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl3') #if needed, place an 'r' before any parameter in order to address any special character such as '\'.
    conn = cx_Oracle.connect(user='system', password='putUrCodeHere', dsn=dsn_tns) #if needed, place an 'r' before any parameter in order to address any special character such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
    
    c = conn.cursor()
    c.execute('select LINK_TIMESTAMP_ID from TRAFFIC_CONGESTION') # use triple quotes if you want to spread your query across multiple lines
    LINK_TIMESTAMP_ID_LIST = []
    for row in c:
        LINK_TIMESTAMP_ID_LIST.append(row[0])

    
    print('LINK_TIMESTAMP_ID_LIST IS ', len(LINK_TIMESTAMP_ID_LIST))
    
    with urllib.request.urlopen("http://feed.opendata.imet.gr:23577/fcd/congestions.json?offset=3000&limit=3000") as url:
        data = json.loads(url.read().decode())
        
        print(data[0])
        print("is of type", type(data[0])) 
#        data[1].split(',')[2]
#        print(data[1].split(',')[2])
    #item_dict = json.l oads(json_data)
        jsonlength = len(data)
        print('jsonlength is ',jsonlength)
        #print(data[0]['Timestamp']) 
        #c2 = conn.cursor()
        for x in range(jsonlength):
            #print(x)
            timest = str(data[x]['Timestamp'].replace('.000', ''))
            LINK_TIMESTAMP_ID = str(data[x]['Link_id'])+'_'+str(data[x]['Link_Direction'])+'_'+timest
            #print(LINK_TIMESTAMP_ID)
            if LINK_TIMESTAMP_ID not in LINK_TIMESTAMP_ID_LIST :
                timestamp = 'TO_TIMESTAMP('+timest+''', 'YYYY-MM-DD HH:MI:SS')'''
                c.execute('''INSERT INTO TRAFFIC_CONGESTION 
                          (LINK_TIMESTAMP_ID, LINK_ID, LINK_DIRECTION,CONGESTION, TIME_STAMP) 
                          VALUES  
                          (:1,:2,:3,:4,TO_TIMESTAMP(:5, 'YYYY-MM-DD HH24:MI:SS'))''',
                          {"1" : LINK_TIMESTAMP_ID, "2" : str(data[x]['Link_id']), "3" : str(data[x]['Link_Direction']),"4" : str(data[x]['Congestion']),"5" : timest})
       
        c.execute('COMMIT')
        
        print('done')

  

def JsonFileToOracle():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl3') #if needed, place an 'r' before any parameter in order to address any special character such as '\'.
    conn = cx_Oracle.connect(user='system', password='26282628', dsn=dsn_tns) #if needed, place an 'r' before any parameter in order to address any special character such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
    
    c = conn.cursor()
    c.execute('select LINK_TIMESTAMP_ID from TRAFFIC_CONGESTION') # use triple quotes if you want to spread your query across multiple lines

    
    path_to_json = 'C:/Users/Mangekyo/Documents/Python Scripts/Json_Tests/jsonfiles/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]
    print(json_files[1])  # for me this prints ['foo.json']
    
    for f_name in json_files:
        with open(f_name) as json_file:
            data = json.load(json_file)
            print(data[0])
            c.execute('select LINK_TIMESTAMP_ID from TRAFFIC_CONGESTION') # use triple quotes if you want to spread your query across multiple lines
            LINK_TIMESTAMP_ID_LIST = []
            for row in c:
                LINK_TIMESTAMP_ID_LIST.append(row[0])
                
            print('LINK_TIMESTAMP_ID_LIST IS ', len(LINK_TIMESTAMP_ID_LIST))
            
            print(data[0])
            print("is of type", type(data[0])) 

            jsonlength = len(data)
            print('jsonlength is ',jsonlength)

            for x in range(jsonlength):
                #print(x)
                timest = str(data[x]['Timestamp'].replace('.000', ''))
                LINK_TIMESTAMP_ID = str(data[x]['Link_id'])+'_'+str(data[x]['Link_Direction'])+'_'+timest
                #print(LINK_TIMESTAMP_ID)
                if LINK_TIMESTAMP_ID not in LINK_TIMESTAMP_ID_LIST :
                    #timestamp = 'TO_TIMESTAMP('+timest+''', 'YYYY-MM-DD HH:MI:SS')'''
                    c.execute('''INSERT INTO TRAFFIC_CONGESTION 
                              (LINK_TIMESTAMP_ID, LINK_ID, LINK_DIRECTION,CONGESTION, TIME_STAMP) 
                              VALUES  
                              (:1,:2,:3,:4,TO_TIMESTAMP(:5, 'YYYY-MM-DD HH24:MI:SS'))''',
                              {"1" : LINK_TIMESTAMP_ID, "2" : str(data[x]['Link_id']), "3" : str(data[x]['Link_Direction']),"4" : str(data[x]['Congestion']),"5" : timest})
           
            c.execute('COMMIT')
            
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            print('done') 

def executeSomething():
    try:
        print(datetime.now())
        JsonOracle.JsonToOracle()  
        time.sleep(850)
    except:
        print("An exception occurred")
      
    

while True:
    executeSomething()   
    
  
            
print('done2')   

