import pdb

import requests
from time import sleep
# from openpyxl import Workbook
import random 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json
import argparse
import sys

iter=0

import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def getAreaCode(areaName):
    translationTable = str.maketrans("éàèùâêîôûç", "eaeuaeiouc")

    resp=requests.get('http://les-departements.fr/carte-des-departements.html')
    soup=BeautifulSoup(resp.content,features='html.parser')
    codeList=soup.find('ul',attrs={'id':'list-1'}).find_all('li')
    for code in codeList:
        codeText=str(code.find('b').text).lower().translate(translationTable)
        if codeText.__contains__(areaName):
            areaCode = codeText.split(' ')[0]
            break
        else:
            continue
    # print('areaCode:',areaCode)
    # sys.exit()
    return areaCode
def saveInFile(csvData):
    global iter
    df = pd.DataFrame(csvData, index=[0])
    if iter == 0:
        df.to_csv('listsCSV.csv', index=False)
        iter = 1
    else:
        df.to_csv('listsCSV.csv', index=False, header=False, mode='a')


try:
    parser = argparse.ArgumentParser()

    #-db DATABASE -u USERNAME -p PASSWORD -size 20000
    parser.add_argument("-what", "--what", dest = "what", default = "restaurant", help="Place Type")
    parser.add_argument("-where", "--where", dest = "where", default = "ding_dong", help="Where ID")

    # csvData = []

    # csvData.append(('business_names','address','category','number','url','website_link','fb_link','SIRET','Code_NAF','Salaries','SIREN','Date_Creation','Capital_Social'))
    # with open('listsCSV.csv', 'w') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerows(csvData)
    #     csvFile.close()


    print("Scraping lists Please Wait..........")
    # whats=soup.find(class_='pj-link')
    args = parser.parse_args()

    # whats="restaurant"
    # wheresid="38"
    whats=args.what
    wheres=args.where

    wheresid=getAreaCode(wheres)

    rows = []
    # first=true
    i=1
    for i in range(1,101):
        # csvData = []
        print(i)
        if i == 0:
            i=1

        print(i)
        # api_url = "https://www.pagesjaunes.fr/annuaire/chercherlespros"
        ou="Is%C3%A8re%20%2838%29"
        # print(ou)
        api_url = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui="+whats+"&idOu=D0"+wheresid+"&ou=Is%C3%A8re%20%2838%29&proximite=0&quoiQuiInterprete="+whats+"&contexte=NN%2B4XFPACNERQeU7pE9jUgxISMRndNFsTX8Pg%2Byl0iE%3D&page="+str(i)
        payload = {'quoiqui':whats,
                    'idOu':"D0"+wheresid,
                    'ou':ou,
                    'proximite':'0',
                    'quoiQuiInterprete':whats,
                    'contexte':'NN%2B4XFPACNERQeU7pE9jUgxISMRndNFsTX8Pg%2Byl0iE%3D',
                    'page':'1'}
        pageabout = requests.get(api_url)
        # response = requests.get(api_url)
        # print(api_url)
        # email=''

        # if pageabout.status_code == 200:
        #     print("No Problem")
        # else:
        #     for row in rows:
        #         csvData.append(row)
        #     df = pd.DataFrame(csvData)
        #     df.to_csv('listsCSV.csv', index=False,mode='a',header=False)
        #     raise Exception("Query failed to run by returning code of {}. {}",pageabout)

        sleep(random.random())
        soup = BeautifulSoup(pageabout.content, 'html.parser')

        # print(soup.get_text)
        #business_details=soup.find_all('article',)
        business_details = soup.find_all ('li',class_='bi-bloc blocs clearfix  bi-pro' )

        business_names=soup.find_all('h3',class_='company-name noTrad')
        address=soup.find_all('div',class_='adresse-container noTrad')
        category=soup.find_all('div',class_='activites-mentions')
        number=soup.find_all('ul',class_='main-contact-container hidden-phone clearfix')
        #pdb.set_trace ()
        # print(address)
        bdlv=[]
        print(len(business_details))
        for bd0 in business_details:
            if bd0.div is not None:
                bd=bd0.div.attrs
                for x, y in bd.items():
                    print(y)
                    if type(y) is str:
                        y= json.loads(y)
                        # print(y['kProCodeEtabToUserInfo'])
                        bdlv.append(y['kProCodeEtabToUserInfo'])

        for j in range(len(business_details)):

            if business_names[j].a.string is not None:
                bn=business_names[j].a.string.strip()
            if address[j].a.string is not None:
                ad=address[j].a.string.strip()
            if category[j].a.string is not None:
                ca=category[j].a.string.strip()
            if number[j].li.div.div is not None:
                conu=number[j].li.div.div.findChildren("strong", recursive=False)
                try:
                    #=conu[0]['title'].string.strip()
                    nu=cleanhtml(str(conu[0]).strip())
                except:
                    nu=''

            print(f"""
bn : {bn}
ad : {ad}
ca : {ca}
conu : {conu}
nu: {nu}


            """)
            # print(bdkl)
            # print(business_names[j].a.string.strip())
            # print(address[j].a.string.strip())
            # print(category[j].a.string.strip())
            # print(number[j].li.div.div.strong)
            # print()
            # print('')
            # ________________________________________________________________________________________________________________________________________________________________________
            api_url = "https://www.pagesjaunes.fr/pros/"+str(bdlv[j])
            pagedetail = requests.get(api_url)
            # if pagedetail.status_code == 200:
            #     print("No Problem")
            # else:
            #     for row in rows:
            #         csvData.append(row)
            #     df = pd.DataFrame(csvData)
            #     df.to_csv('listsCSV.csv', index=False,mode='a',header=False)
            #     raise Exception("Query failed to run by returning code of {}. {}")

            i=i-1
            print(i)
            sleep(random.random())
            soup = BeautifulSoup(pagedetail.content, 'html.parser')
            SIREN=""
            SIRET=""
            Code_NAF=""
            Salaries=""
            FormeJuridique=""
            Date_Creation=""
            Capital_Social=""
            if soup.find('div',class_='row siret') is not None:
                SIRET=soup.find('div',class_='row siret').span.string.strip()
                # print(SIRET)
            if soup.find('div',class_='row naf') is not None:
                Code_NAF=soup.find('div',class_='row naf').span.string.strip()
                # print(Code_NAF)
            if soup.find('div',class_='row effectif') is not None:
                Salaries=soup.find('div',class_='row effectif').span.string.strip()
                # print(Salaries)
            if soup.find('div',class_='row siren') is not None:
                SIREN=soup.find('div',class_='row siren').span.string.strip()
                # print(SIRET)
            if soup.find('div',class_='row forme_juridique') is not None:
                FormeJuridique=soup.find('div',class_='row forme_juridique').span.string.strip()
                # print(FormeJuridique)
            if soup.find('div',class_='row date_creation_entreprise') is not None:
                Date_Creation=soup.find('div',class_='row date_creation_entreprise').span.string.strip()
                # print(Date_Creation)
            if soup.find('div',class_='row capital_social') is not None:
                Capital_Social=soup.find('div',class_='row capital_social').span.string.strip()
                # print(Capital_Social)
            links=soup.find_all('li',class_='marg-btm-xs premiere-visibilite')


            fb_link=''
            website_link=''
            if len(links)==1:
                website=links[0].find('a').find_all('span')
                website_link=website[1].string.strip()
                # print(website[1].string.strip())
            if len(links)==2:
                fb=links[1].find('a').find_all('span')
                fb_link=(fb[1].string.strip())
                # print(fb[1].string.strip())
            # print(bdlv[j])


            #  =


            # ________________________________________________________________________________________________________________________________________________________________________
            # _row=(bn,ad,ca,nu,bdlv[j],website_link,fb_link,SIRET,Code_NAF,Salaries,SIREN,Date_Creation,Capital_Social)
            # rows.append(_row)
            # csvData.append(_row)
            csvData={'business_names':bn,'address':ad,
            'category':ca,'number':nu,'url':bdlv[j],
            'website_link':website_link,'fb_link':fb_link,
            'SIRET':SIRET,'Code_NAF':Code_NAF,'Salaries':Salaries,
            'SIREN':SIREN,'Date_Creation':Date_Creation,'Capital_Social':Capital_Social
            }
            saveInFile(csvData)
            #print(csvData)
        # df = pd.DataFrame(csvData)
        # df.to_csv('listsCSV.csv', index=False,mode='a',header=False,encoding='utf-8-sig')

    #             # for row in rows:
    #     # csvData.append(_row)
    #     # sheet.append(_row)
except ValueError:
    print("Error")
