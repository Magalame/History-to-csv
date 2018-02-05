# -*- coding: utf-8 -*-

"""
Created on Sat Oct 21 16:01:36 2017
"""

import sqlite3
import sys
import os
import argparse
import csv
import json

parser = argparse.ArgumentParser()

parser.add_argument("-b", "--browser", help="Which browser you want to extract your history from")

args = parser.parse_args()


if not args.browser:
    pass
elif args.browser.lower() == "chrome":
    path = os.getenv('APPDATA') + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\"
elif args.browser.lower() == "vivaldi":
    path = os.getenv('APPDATA') + "\\..\\Local\\Vivaldi\\User Data\\Default\\"
    
def check_availability(cursor, tablename):
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #lists all tables
    except Exception as e:
        if "database is locked" == str(e):
            print("You need to close your browser first, can't access the database")
            sys.exit(0)
        else:
            print(e)
        
    result = cursor.fetchall() 

    for var_tuple in result: #looks for "urls" in the list of tables, because that's where the urls are stored 
    #print(var_tuple)
        if tablename in var_tuple:
            return True
            
    return False

def get_content_table(cursor,tablename):
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #lists all tables
    except Exception as e:
        if "database is locked" == str(e):
            print("You need to close your browser first, can't access the database")
            sys.exit(0)
        else:
            print(e)
        
    result = cursor.fetchall() 
    found = False
    for var_tuple in result: 
        
        if tablename in var_tuple:
            found = True
            break
    if not found:
        print("Can't find the good table in the database")
        sys.exit(0)
    
    cursor.execute("select * from " + tablename + ";") #gets the content
    result = cursor.fetchall()
    
    return result
    
def wrapper_get_content_table(filename, tablename):
    
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    res = get_content_table(c,tablename)
    conn.commit()
    conn.close()
    return res

def extract_history(path):    

    return wrapper_get_content_table(path + 'History',"urls")
    
            
def save_history_csv(path, namefile, remove_null_timestamp = True):
    
    """Save the history from path in a file with the csv format"""
    
    if os.path.isfile(namefile):
        answer = ""
        while answer.lower() != 'y' and answer.lower() != 'n':
            answer = input(namefile + " already exist, do you want to overwrite it?")
            
    
        if answer == "n":
            return False
    
    history = extract_history(path)
    
    with open(namefile, "w", newline='',encoding='utf-8') as pfile:
        
        csv_writer = csv.writer(pfile)

        csv_writer.writerow(['id','url', 'title','visit_count', 'typed_count', 'last_visit_time','hidden'])
        
        if remove_null_timestamp:
            for row in history:
                if row[-2] != 0: 
                    csv_writer.writerow(row)
        else:
            for row in history:
                csv_writer.writerow(list(row))
              

def list_to_dict(liste):
    
    out = []
    
    for row in liste:
        tmp = {}
        tmp['id'] = row[0]
        tmp['url'] = row[1]
        tmp['title'] = row[2]
        tmp['visit_count'] = row[3]
        tmp['typed_count'] = row[4]
        tmp['last_visit_time'] = row[5]
        tmp['hidden'] = row[6]
        out.append(tmp)
        
    return out
    
    
    