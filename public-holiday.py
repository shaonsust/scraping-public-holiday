import requests
import html5lib
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json

def getContent(url):
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')

    return soup

def publicHoliday():
    result = {}
    date_format = '%d %b %Y'

    # Taking all country name and its html page
    countries, countryPages = countryList()

    for i in range(len(countryPages)):
        data = {}

        # Getting 6 years data 
        for year in range(2017, 2023):
            # Set the url for scraping data
            url = "https://www.timeanddate.com" + str(countryPages[i] + str(year))

            # Parse HTML and save BeautifulSoap object
            soup = getContent(url)
            
            # Find table
            table = soup.find('table', {'id' : 'holidays-table'})
            if table is None:
                continue

            # Find all tr
            trs = table.find('tbody').findAll('tr')
            temp = []

            # Find all td from trs
            for tr in trs:
                item = []
                dic = {}
                th = tr.find('th')

                if th is None:
                    continue
                
                if th is not None:
                    str_date = th.text.encode('utf-8') + ' ' + str(year)
                    date_obj = datetime.strptime(str_date, date_format)
                    item.append(date_obj.strftime('%Y-%m-%d %H:%M:S'))
            
                # continue
                tds = tr.findAll('td')

                for td in tds:
                    # data[contry][year].append(td.text)
                    # text = td.text
                    
                    text = re.sub('[^A-Za-z0-9()''\']+', ' ', td.text.encode('utf-8'))
                    if len(text) > 0 :
                        item.append(text)
                    else:
                        item.append('')

                # Find and get description of holiday url
                if len(item) == 4:
                    item.append('')
                        
                a = tr.find('a')
                if a is not None:
                    thref = a.attrs.get('href')
                    href = 'https://www.timeanddate.com' + thref
                    item.append(href)
                else:
                    item.append('')
        
                if len(item) == 6:
                    dic['day'] = item[0]
                    dic['weekDay'] = item[1]
                    dic['name'] = item[2]
                    dic['type'] = item[3]
                    dic['location'] = item[4]
                    dic['detailsURL'] = item[5]
                    temp.append(dic)

            # Assign data 
            data[year] = temp
            print("Scraping country and year : " + str(countries[i]) + " and " + str(year))
                                                     
        result[countries[i]] = data

    print("Complete.....")

    # Write json data into a json file
    with open('global_public_holiday.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def countryList():
    html = getContent('https://www.timeanddate.com/holidays/')

    uls = html.findAll("ul", {'class': 'category-list__list'})

    # Declare an array for putting country name and html pages name
    countryList = []
    linkList = []

    # Extracting contry name from options
    for ul in uls:
        anchors = ul.findAll('a')
        for a in anchors:
            countryList.append(a.text.strip().encode('utf-8'))
            linkList.append(a.attrs.get('href'))

    return [countryList, linkList]

def getCountryListInJsonFile():
    countries = countryList()

    with open('country_list.json', 'w') as f:
        json.dump(countries[0], f, ensure_ascii=False, indent=4)

publicHoliday()
# getCountryListInJsonFile()
