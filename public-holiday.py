import requests
import html5lib
from bs4 import BeautifulSoup
import array
import re
import json

def getContent(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

def publicHoliday():
    result = {}

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
                th = tr.find('th')
                if th is not None:
                    item.append(th.text.encode('utf-8'))
            
                # continue
                tds = tr.findAll('td')

                for td in tds:
                    # data[contry][year].append(td.text)
                    text = re.sub('[^A-Za-z0-9()'']+', ' ', td.text.encode('utf-8'))
                    item.append(text)

                # Find and get description of holiday url
                a = tr.find('a')
                if a is not None:
                    thref = a.attrs.get('href')
                    href = 'https://www.timeanddate.com' + thref
                    item.append(href)

                if len(item) > 0:
                    temp.append(item)

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
getCountryListInJsonFile()
