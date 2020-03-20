from countriesWithCodes import countryDict
import re
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd
import traceback
import CoronaTexts


# get
# open up countryCodeParser
"""
scrape the population webpage (keep in mind that we update all countries at once)
make the http request
for each country
    if the country is in the countryDict
        convert the value in the dict to a list and append the country.population in http

:return:
"""
def updatePops(coronaTexts):

    URL = "https://worldpopulationreview.com/"
    page = requests.get(URL)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    countryName = ""
    countryPop = 0
    # 1 to skip the header
    for t in range(1, len(tr_elements)):
        countryData = tr_elements[t]
        cellIdx = 0
        for cell in countryData.iterchildren():
            # content in 2nd col is country name
            if cellIdx == 1:
                countryName = str(cell.text_content())
                # need to normalize some
                if countryName == "Bolivia":
                    countryName = "Bolivia (Plurinational State of)"
                elif countryName == "Falkland Islands":
                    countryName = "Falklands"
                elif countryName == "Ivory Coast":
                    countryName = "Côte d'Ivoire"
                elif countryName == "Brunei":
                    countryName = "Brunei Darussalam"
                elif countryName == "United Arab Emirates":
                    countryName = "UAE"
                elif countryName == "United Kingdom":
                    countryName = "UK"
                elif countryName == "United States":
                    countryName = "USA"

            elif cellIdx == 2:
                numWithCommas = str(cell.text_content())
                groupsBetweenCommas = numWithCommas.split(',')
                joinGroups = "".join(groupsBetweenCommas)
                countryPop = "".join(cell.text_content().split(','))
            elif cellIdx != 0:
                break
            cellIdx += 1

        # we now have a name of a country and a population
        for country in coronaTexts.countries:
            if country.getCountryName() == countryName:
                CoronaTexts.cPrint("Updating {}'s population...".format(countryName))
                prevPop = country.getPopulation()
                country.setPopulation(countryPop)
                CoronaTexts.cPrint("Updated population for {}.".format(countryName))
                CoronaTexts.cPrint("Population at previous update: {}".format(str(prevPop)))
                CoronaTexts.cPrint("Most recent population: {}".format(countryPop))
                break
        for code in countryDict:
            name = countryDict[code]    # name is value we are comparing countryName against

            # # if the value[key] is already a list, just edit the value
            # if isinstance(name, list):
            #     countryDict[code][1] = countryPop
            # el
            if isinstance(name, str):
                # need to transform it into a list
                try:
                    # exceptions
                    if name == "Congo Republic":
                        # make it match the incoming name
                        name = "Republic of the Congo"
                    # elif name ==
                    if countryName == name:
                        # append the number as a string
                        namePopAppended = []
                        namePopAppended.append(name)
                        namePopAppended.append(int(countryPop))
                        # store it back to the dict for CoronaTexts to use
                        countryDict[code] = namePopAppended
                except ValueError:
                    print(traceback.format_exc())


    htmlText = requests.get(URL).text
    soup = BeautifulSoup(htmlText, 'html.parser')

    tbody = 0
    for country_tbody in soup.find_all('tbody'):

        for country_tr in country_tbody.find_all('tr'):
            for country_td in country_tr.find_all('td'):
               pass


def main():
    # create isolated corona texts env
    coronaTexts = CoronaTexts()
    coronaTexts.refreshPopulations()


if __name__ == '__main__':
    main()

