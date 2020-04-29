# -*- coding: utf-8 -*-
import sqlite3
import csv
import json
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template
from secret import client_id
from secret import client_secret


### Part 1: Scrap Data

#def cache_uni_list():
CACHE_FNAME_1 = 'cache_university_list.json'
try:
    cache_file = open(CACHE_FNAME_1, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION_1 = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION_1 = {}

#def cache_uni_wiki():
CACHE_FNAME_2 = 'cache_university_wiki.json'
try:
    cache_file = open(CACHE_FNAME_2, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION_2 = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION_2 = {}


#use data in cache file to find universities, if it has cache, then use the cache data
#else useAPI to get data in wiki and cache
def find_university_list_using_cache(CACHE_DICTION_1):
    baseurl = 'https://en.wikipedia.org/w/api.php'
    paras = {}
    paras['action']='parse'
    paras['page']='List_of_state_and_territorial_universities_in_the_United_States'
    paras['format']='json'

#    CACHE_DICTION = cache_uni_list()

    if 'universitylist' in CACHE_DICTION_1:
        return CACHE_DICTION_1["universitylist"]

    else:
        output = json.loads(requests.get(baseurl,paras).text)
        content = output['parse']['text']['*']
        CACHE_DICTION_1['universitylist'] = content
        dumped_json_cache = json.dumps(CACHE_DICTION_1)
        fw = open('cache_university_list.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION_1['universitylist']

def scrap_university_list(page_text):
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content = page_soup.find(class_='mw-parser-output')
#    content1 = content.find(class_='tocright')
#    content2 = content1.find_all('li')
    #statelist = []
    contentlist = []
#    universitylist = []
    #for i in content2:
    #    content3 = str(i).split('#')
    #    content4 = (str(content3[1]).split('"'))[0]
    #    statelist.append(content4)
    #for i in statelist:
    content5 = content.find_all('ul')
    for i in content5[5:]:
        items = (str(i).split('title'))
        for ii in items:
            try:
                finalitem = ((ii.split('a href="')[1]).strip('/wiki/'))
                finalitem1 = finalitem.strip('"')
                finalitem2 = finalitem1[:-2]
                contentlist.append(finalitem2)
            except:
                pass
    return contentlist

def find_university_using_cache(university,CACHE_DICTION_2):
    baseurl = 'https://en.wikipedia.org/w/api.php'
    paras = {}
    paras['action']='parse'
    paras['page']=university
    paras['format']='json'

#    CACHE_DICTION = cache_uni_wiki()

    if university in CACHE_DICTION_2:
#        print("Getting cached wiki data...")
        return CACHE_DICTION_2[university]
    else:
        print("Making a request for new wiki data...")
        output = json.loads(requests.get(baseurl,paras).text)
        content = output['parse']['text']['*']
        CACHE_DICTION_2[university] = content
        dumped_json_cache = json.dumps(CACHE_DICTION_2)
        fw = open('cache_university_wiki.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION_2[university]

def scrap_university_info(page_text):
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content = page_soup.find(class_='infobox vcard')
    content1 = content.find_all('tr')
    infodic = {}
    for i in content1:
        try:
            name = i.find('th').text
            detail = i.find('td').text
            infodic[name] = detail
        except:
            pass
    try:
        infodic['geoinfo'] = content.find(class_='geo-dec').text
    except:
        pass

    finaldic = {}

    try:
        finaldic['University'] = content.find(class_='fn org').text
    except:
        finaldic['University'] = 'NULL'
    try:
        finaldic['Motto'] = infodic['Motto']
    except:
        finaldic['Motto'] = 'NULL'
    try:
        finaldic['Type'] = infodic['Type']
    except:
        finaldic['Type'] = 'NULL'
    try:
        finaldic['Established'] = infodic['Established']
    except:
        finaldic['Established'] = 'NULL'
    try:
        finaldic['Website'] = infodic['Website']
    except:
        finaldic['Website'] = 'NULL'
    try:
        finaldic['geoinfo'] = infodic['geoinfo']
    except:
        finaldic['geoinfo'] = 'NULL'
    return finaldic


### Part 2: Write into Database

DBNAME = 'univeristy.db'
rankingsfile = '2019-QS-World-University-Rankings2.csv'

def createdb(DBNAME):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        DROP TABLE IF EXISTS 'Wiki';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Rankings';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Wiki' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'University' TEXT,
            'Motto' TEXT,
            'Type' TEXT,
            'Established' TEXT,
            'Website' TEXT,
            'geoinfo' TEXT
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Rankings' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                '2019 Rank' INTEGER,
                '2018 Rank' INTEGER,
                'University Name' TEXT,
                'Region' TEXT,
                'Size' TEXT,
                'Focus' TEXT,
                'RES' TEXT,
                'AGE' TEXT,
                'STATUS' TEXT,
                'Academic Reputation Score' TEXT,
                'Academic Reputation Rank' TEXT,
                'Employer Reputation Score' TEXT,
                'Employer Reputation Rank' TEXT,
                'Student Score' TEXT,
                'Student Rank' TEXT,
                'Citations Score' TEXT,
                'Citations Rank' TEXT,
                'International Faculty Score' TEXT,
                'International Faculty Rank' TEXT,
                'International Students Score' TEXT,
                'International Students Rank' TEXT,
                'Overall Score' TEXT,
                FOREIGN KEY ('University Name') REFERENCES Wiki('University')
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def writeintorankings(DBNAME):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    with open (rankingsfile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f,delimiter=',')
#        rownumber = 0
        for row in reader:
            insertion = (None,row[0], row[1], row[2].lower(), row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21])
        #insertion = (None,'N/A', 'N/A', 'UNIVERSITY OF CALIFORNIA, SAN FRANCISCO (UCSF)', 'S', 'SP', 'VH', '5', 'A', '51.5', '145', '21.8', '435', '100', '2', '61.1', '149', '48', '335', '-', '-', '-')
            statement = "INSERT INTO 'Rankings'"
            statement += 'VALUES (?,?, ?, ?, ?, ?, ?,?,?, ?, ?, ?, ?, ?,?,?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def writeintowiki(DBNAME,CACHE_DICTION_1,CACHE_DICTION_2):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = scrap_university_list(find_university_list_using_cache(CACHE_DICTION_1))
    for item in list1:
        try:
            i = scrap_university_info(find_university_using_cache(item,CACHE_DICTION_2))
            insertion = (None,i['University'].lower(),i['Motto'],i['Type'],i['Established'],i['Website'],i['geoinfo'])
            statement = 'INSERT INTO "Wiki"'
            statement += 'VALUES (?,?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
        except:
            pass
    conn.commit()
    conn.close()

### def the function calls all above to scrap webs and write into databse
def createbdall(DBNAME,CACHE_DICTION_1,CACHE_DICTION_2):
    createdb(DBNAME)
    writeintorankings(DBNAME)
    writeintowiki(DBNAME,CACHE_DICTION_1,CACHE_DICTION_2)


### Part 3: Output
CACHE_FNAME3 = 'cache_idlist.json'

try:
    cache_file = open(CACHE_FNAME3, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def find_idlist_using_cache():
    baseurl = 'https://api.foursquare.com/v2/venues/categories'
    paradic = {}
    paradic['client_id'] = client_id
    paradic['client_secret'] = client_secret
    paradic['v'] = '20191103'
    unique_ident = paradic['v']
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        output = json.loads(requests.get(baseurl,params=paradic).text)
        idoutput2 = output['response']['categories']
        iddic = {}
        for i in idoutput2:
            list = i['categories']
            for ii in list:
                name = ii['name'].lower()
                id = ii['id']
                iddic[name] = id
        CACHE_DICTION[unique_ident] = iddic
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME3,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


CACHE_FNAME4 = 'cache.json'

try:
    cache_file2 = open(CACHE_FNAME4, 'r')
    cache_contents2 = cache_file2.read()
    CACHE_DICTION2 = json.loads(cache_contents2)
    cache_file2.close()
except:
    CACHE_DICTION2 = {}

def make_request_using_cache(near_item,categoryId_item):
#    baseurl = 'https://api.foursquare.com/v2/venues/search'
    paradic = {}
    idlookup = find_idlist_using_cache()
    paradic['near'] = (near_item).lower()
    paradic['categoryId'] = idlookup[(categoryId_item).lower()]
    paradic['limit'] = 25
    paradic['client_id'] = client_id
    paradic['client_secret'] = client_secret
    paradic['v'] = '20191103'
    unique_ident = str(paradic['near'])+str(paradic['categoryId'])
    if unique_ident in CACHE_DICTION2:
        return CACHE_DICTION2[unique_ident]
    else:
        CACHE_DICTION2[unique_ident] = search(near_item,categoryId_item)
        dumped_json_cache = json.dumps(CACHE_DICTION2)
        fw = open(CACHE_FNAME4,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION2[unique_ident]

def search(near_item,categoryId_item):
    baseurl = 'https://api.foursquare.com/v2/venues/search'
    paradic = {}
    idlookup = find_idlist_using_cache()
    paradic['near'] = (near_item).lower()
    paradic['categoryId'] = idlookup[(categoryId_item).lower()]
    paradic['limit'] = 25
    paradic['client_id'] = client_id
    paradic['client_secret'] = client_secret
    paradic['v'] = '20191103'
    result = requests.get(baseurl,params=paradic).text
    response = json.loads(result)
    respon = response['response']
    return respon

def getdata(near_item,categoryId_item):
    output = make_request_using_cache(near_item,categoryId_item)
    venueslist = []
    for i in output['venues']:
        venuesdicitem = {}
        venuesdicitem['id'] = i['id']
        venuesdicitem['venue'] = i['name']
        venuesdicitem['address'] = i['location']['formattedAddress']
        venuesdicitem['lat'] = i['location']['lat']
        venuesdicitem['lng'] = i['location']['lng']
        venueslist.append(venuesdicitem)
    return venueslist


def db_list(orderby):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    insertion = 'SELECT Wiki.University, Wiki.Motto, Wiki.Type, Wiki.Established, Wiki.Website FROM Wiki'
    if orderby.lower() == 'name':
        order =' ORDER BY Wiki.University '
        cur.execute(insertion+order)
        item = cur.fetchall()
        return item
    if orderby.lower() == 'established':
        order =' ORDER BY Wiki.Established '
        cur.execute(insertion+order)
        item = cur.fetchall()
        return item
    else:
        pass
    cur.close()

def db_score():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    insertion = 'SELECT Region, AVG(Rankings."Overall Score") AS avg, COUNT(*) as num FROM Rankings GROUP BY Rankings.Region '
    order = ' ORDER BY avg DESC '
    cur.execute(insertion+order)
    item = cur.fetchall()
    return item
    cur.close()

def db_rank(orderby):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    insertion = 'SELECT * FROM Rankings WHERE Region="United States"'
    if orderby.lower() == '2019 rank':

        cur.execute(insertion)
        item = cur.fetchall()
        return item
    if orderby.lower() == '2018 rank':
        order =' ORDER BY "2018 Rank" '
        cur.execute(insertion+order)
        item = cur.fetchall()
        return item
    else:
        pass
    cur.close()

def db_website(university):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    insertion = 'SELECT Website FROM Wiki WHERE University="'
    insertion += university.lower()+'"'
    cur.execute(insertion)
    item = cur.fetchone()
    return item
    cur.close()

def db_map(university):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    insertion = 'SELECT geoinfo FROM Wiki WHERE University="'
    insertion += university.lower()+'"'
    cur.execute(insertion)
    item = cur.fetchone()
    return item
    cur.close()


app = Flask(__name__)
@app.route('/nearbycafe/<university>')
def nearby(university):
    try:
        headlines=getdata(university,'caf\u00e9')
        return render_template('nearby.html', university=university, headlines=headlines)
    except:
        return render_template('error.html')

@app.route('/universitylist/<order>')
def list(order):
    try:
        headlines = db_list(order)
        return render_template('name.html', headlines = headlines)
    except:
        return render_template('error.html')

@app.route('/score')
def score():
    try:
        headline = db_score()
        headlines = {}
        for i in range(len(headline)):
            headlines[i] =(headline[i][0],round(int(headline[i][1])),headline[i][2])
        return render_template('score.html', headlines = headlines)
    except:
        return render_template('error.html')

@app.route('/universityrankings/<order>')
def rank(order):
    try:
        headlines = db_rank(order)
        return render_template('rank.html', headlines = headlines)
    except:
        return render_template('error.html')

@app.route('/website/<university>')
def website(university):
    link = db_website(university)
    link2 = 'https://'+str(link)[2:-3]
    if link != None:
        return render_template('website.html', headlines = link2, university=university)
    else:
        return render_template('error.html')


@app.route('/map/<university>')
def map(university):
    try:
        geoinfo = db_map(university)
        link2 = 'https://www.google.com/maps/place/'+str(geoinfo)
        return render_template('map.html', headlines = link2)
    except:
        return render_template('error.html')

if __name__=="__main__":
#    createbdall(DBNAME,CACHE_DICTION_1,CACHE_DICTION_2)
    app.run()
