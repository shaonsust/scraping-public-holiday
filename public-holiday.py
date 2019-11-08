import requests
import html5lib
from bs4 import BeautifulSoup
import array
import re
import json

def publicHoliday():
    result = {}

    # Taking all country name and its html page
    countries, countryPages = countryList()

    for i in range(len(countryPages)):
        data = {}

        # Getting 15 years data 
        for year in range(2015, 2030):
            # Set the url for scraping data
            url = "https://www.qppstudio.net/publicholidays" + str(year) + "/" + str(countryPages[i])

            # Connect to the url
            response = requests.get(url)

            # Parse HTML and save BeautifulSoap object
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find table
            table = soup.find('table')

            # Find all tr
            trs = soup.findAll('tr')
            temp = []

            # Find all td from trs
            for tr in trs:
                tds = tr.findAll('td')
                item = []
                for td in tds:
                    # data[contry][year].append(td.text)
                    text = re.sub('[^A-Za-z0-9()]+', ' ', td.text)
                    item.append(text)
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
    # Open country.html file and get its source code
    f = open('country.html', 'r')
    html = f.read()
    f.close()

    # Make soup object from html string
    soup = BeautifulSoup(html, 'html.parser')

    # Find all option here
    options = soup.find("select").findAll("option")

    # Declare an array for putting country name and html pages name
    countryList = []
    linkList = []

    # Extracting contry name from options
    for option in options:
        countryList.append(option.text.strip())
        linkList.append(option.attrs.get('value'))

    return [countryList, linkList]

publicHoliday()
