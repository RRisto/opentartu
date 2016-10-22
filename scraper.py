#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/estnltk/pyvabamorf
# pip install pyvabamorf


from os import chdir
chdir(r"C:\Users\Risto\Documents\GitHub\opentartu")

import re, sys, subprocess, urllib2
from operator import itemgetter
from collections import OrderedDict
from pprint import pprint
    
def dl_doc(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()
    
def parse_doc(data):
    doc = {}
    html_title = re.search("(<title>)(.*?)(</title>)", data)
    if html_title:
        doc["html_title"] = html_title.group(2)
    text_title = re.search("(<table.*?>)(.*?)(<table.*?>)", data, re.DOTALL).group(2).split("</font>")
    doc["type_title"] = strip_html(text_title[0]).strip()
    doc["text_title"] = strip_html(text_title[1]).strip()
    header = re.search('(<hr .*?>)(.*?)(<hr .*?>)', data, re.DOTALL).group(2)
    doc["header"] = get_hfields(header)
        
    return doc
    
def strip_html(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def get_hfield(header, name):
    return re.search("<tr.*?>" + name + ".*?</tr>", data)
    
def get_hfields(header):
    data = re.findall("<tr.*?>.*?</tr>", header, re.DOTALL)
    
    fields = {}
    
    for field in data:
        infos = {}
        sep = re.split("</font>.*?</td>", field)
        if len(sep)==1:
            continue
        #print sep
        key = strip_html(sep[0]).strip()
        #print key
        values = sep[1].split("<br>")
        for value in values:
            if len(strip_html(value).strip()) != 0:
                infos["text"] = strip_html(value).strip()
            url = re.findall("href=\".*?\"", value)
            if len(url) > 0:
                infos["url"] = re.search("(\")(.*)(\")", url[0]).group(2)
            #print infos["text"]
            fields[key] = infos
        
    return fields

def scrape_url(url):
    data = dl_doc(url)
    doc = {}
    doc["url"] = url
    full_doc = doc.copy()
    full_doc.update(parse_doc(data))
    
    return full_doc

url = "http://info.raad.tartu.ee/webaktid.nsf/gpunid/G533513B3611D3A1FC2257FE3001F2638?OpenDocument"

#if len(sys.argv) >= 2:
#	url = sys.argv[1]

#with open("akt.html") as f:
#    data = f.read()

res = scrape_url(url)

pprint(res)
type(res)
res.keys()

res['text_title']

##proovime esimese tabeli alla scrapeida
import requests
from bs4 import BeautifulSoup
 
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
headers = {'User-Agent': user_agent}
r = requests.get("http://www.tartu.ee/?page_id=1256&lang_id=1&menu_id=2&lotus_url=/webaktid.nsf/WebOtsused?OpenView&Start=1&Count=400&RestrictToCategory=Tartu_Linnavolikogu_8._koosseis_(alates_20.10.13)",headers=headers)
resp = r.content
soup = BeautifulSoup(resp, "html.parser")
for i in soup.findAll("li"):
    Otsuse_url=i.find("a").get("href")
    print(Otsuse_url)

len(Otsuse_url)
type(Otsuse_url)

############################################
##regex
import re as re
string='Tartu Linnavolikogu 13.10.2016 otsus nr  390 \"Loa andmine Narva mnt 177 äriruumi üürilepingu sõlmimiseks\"'

#maanteega aadressi üles
result = re.search("([A-z]+\smnt\s[0-9]+)", string)

if result:
    found = result.group(1)
 #tänav
string='Maa-alade Timuti tn 56, Aardla t\xe4nav T26 ja Vaksali t\xe4nav T36 munitsipaalomandisse taotlemine'
result = re.search("([A-z]+\st\xe4nav\s[A-z|0-9]+)", string)

if result:
    found = result.group(1)
print(found)

string='Kalda tee 1c ja Ihaste tee 3 kruntide detailplaneeringu vastuvõtmine ja avalikule väljapanekule suunamine'
result = re.search("([A-z]+\stee\s[A-z|0-9]+)", string)

if result:
    found = result.group(1)
print(found)
#loeme andmed sisse
import pandas
from geopy.geocoders import Nominatim
import requests
import json
#andmed sisse
data=pandas.read_csv("output2_minu2.csv", sep=";",error_bad_lines=False)
#data=pandas.read_csv("output2.csv", sep=" ",encoding="utf-8",error_bad_lines=False)
list(data.columns.values)
len(data.columns)
data.shape
data["Pealkiri"][6]

#loobime eraldi muutujasse
data["aadressid"]=""
for i in range(data.shape[0]):
    string=data["Pealkiri"][i]
    result = re.search("([A-z]+\st\xe4nav\s[A-z|0-9]+)", string) #tänav
    if result:
        found = result.group(1)
    else:
        result = re.search("([A-z]+\smnt\s[0-9]+)", string)
        if result:
            found = result.group(1)
        else:      
            result = re.search("([A-z]+\stee\s[0-9]+)", string)
            if result:
                found = result.group(1)
            else:
                result = re.search("([A-z]+\stn\s[0-9]+)", string)
                if result:
                    found = result.group(1)
                else:
                    result = re.search("([A-z]+\spst\s[0-9]+)", string)
                    if result:
                        found = result.group(1)
                    else:
                        found=""
    print(found)
    data["aadressid"][i]=found

http://inaadress.maaamet.ee/inaadress/gazetteer?callback=jQuery21402625822420075238_1477125349264&address=tartu+&results=10&appartment=1&unik=0&features=EHAK,TANAV,EHITISHOONE,KATASTRIYKSUS
http://inaadress.maaamet.ee/inaadress/gazetteer?callback=jQuery21402625822420075238_1477125349265&address=tartu+Veski+tn+57&results=10&appartment=1&unik=0&features=EHAK,TANAV,EHITISHOONE,KATASTRIYKSUS
#paneme x ja y koordinaadi juurde
from geopy.geocoders import Nominatim
import time
import json
data["x"]=""
data["y"]=""
data["taisaadress"]=""

for i in range(data.shape[0]):
    if data["aadressid"][i]=="":
        print(i)
    else:
         print(i,data["aadressid"][i])
         url = "http://inaadress.maaamet.ee/inaadress/gazetteer?address="+"Tartu,"+str(data["aadressid"][i])
         time.sleep(0.5)
         try:
             r = requests.get(url)
             j = r.content
             json_str = j.decode("utf-8")
             parsed_json = json.loads(json_str)
             adresses = parsed_json["addresses"][0]
             url="http://www.maaamet.ee/rr/geo-lest/url/?xy="+adresses["viitepunkt_x"]+","+ adresses["viitepunkt_y"]
             try:
                 j = requests.get(url).content.decode("utf-8")
                 data.loc[i,"x"]=j.split(",")[0]
                 data.loc[i,"y"]=j.split(",")[1]
                 data.loc[i, "taisaadress"] = adresses["taisaadress"]
             except:
                 data.loc[i,"x"]=""
                 data.loc[i,"y"]=""
                 data.loc[i, "taisaadress"]=""
                 continue
         except:
             data.loc[i,"x"]=""
             data.loc[i,"y"]=""
             data.loc[i, "taisaadress"]=""
             continue

#mitmel on koordinaadid olemas
data[(data.taisaadress != "")].shape
data2=data[["taisaadress", "x","y"]]
#salvesta (mingi kodeeringu jama kui terve tabeli tahan jagada)
data2.to_csv("output2_koordin.csv", sep=";", encoding="utf-8")





