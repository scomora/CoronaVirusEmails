from CoronaTexts import CoronaTexts, Timeline

def getAndParseCountryCodes():
    f = open("countriesWithCodes.py", "w")

    coronaTextsSample = CoronaTexts()
    coronaTextsSample.getAllCountryCodes()
    lineInFile = ""
    lineInFile += "countryDict = {\n"
    print(lineInFile)
    numCountries = len(coronaTextsSample.countries)
    for country in coronaTextsSample.countries:

        change = "\t\"{}\": \"{}\"".format(country.getCountryCode(), country.getCountryName())
        print(change)
        lineInFile += change
        if numCountries > 1:  # last one
            change = ","
            print(change)
            lineInFile += change
        change = "\n"
        print(change)
        lineInFile += change
        numCountries -= 1
    change = "}"
    lineInFile += change

    f.write(lineInFile)
    f.close()

def main():
    #getAndParseCountryCodes()

    timeline = Timeline()
    timeline.fetchAndUpdateFullTimeline()


if __name__ == '__main__':
    main()