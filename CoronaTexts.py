from enum import Enum

import Messaging
import os
from countriesWithCodes import countryDict
import helpers
import requests
import VirusTrackerAPIHandler
import json
from datetime import datetime, timedelta
import time
import countryPopulationScraper

debugMode = False

availableStats = ["total_cases",
                  "total_recovered",
                  "total_unresolved",
                  "total_deaths",
                  "total_new_cases_today",
                  "total_new_deaths_today",
                  "total_active_cases",
                  "total_serious_cases"]

notificationHeader = """
                    <html>
                    <head></head>
                    <body>
                        <h1>Here are coronavirus statistics for each country.</h1>
                        <ul>Countries:

                    """

"""
    Things to analyze:
    ------------------------------------------
+   if a country's cases are subsiding
+   if there's a significant change compared 
    to the last (maybe store prev/curr diffs?) 
+   if a country's deaths surpass {X}
+   
"""


def getFullTimeline():
    pass


def getCountryTotals(countryCode):
    URL = "https://thevirustracker.com/free-api?countryTotal="
    fullURL = "".join([URL, countryCode])
    r = requests.get(url=fullURL)
    data = r.json()
    return data


def attrToStr(attribute):
    words = attribute.split("_")
    # capitalize first word
    # words[0] = words[0].capitalize()
    return " ".join(words)

class APIStatus(Enum):
    API_DOWN = 1
    API_RUNNING = 2

class CoronaTexts:
    def __init__(self):
        self.countries = []
        self.emailAddressesToReachOutTo = []
        self.Session = Messaging.Session()
        self.apiStatus = APIStatus.API_DOWN

    def isAPIDown(self):
        if self.apiStatus == APIStatus.API_DOWN:
            return True
        else:
            return False

    def setAPIStatus(self, apiStatus):
        self.apiStatus = apiStatus

    def getAPIStatus(self):
        return self.apiStatus

    def getAllCountryCodes(self):
        countryCode = ""
        countryLabel = ""
        allCountryData = getFullTimeline()[0]['data']

        for countryEntry in allCountryData:
            countryCode = countryEntry['countrycode']
            countryLabel = countryEntry['countrylabel']
            newCountry = Country(countryLabel, countryCode)
            self.countries.append(newCountry)

    def constructCountries(self):
        for countryCode in countryDict:
            countryName = countryDict[countryCode]
            country = Country(countryName, countryCode)
            self.countries.append(country)

    def showAllEmailAddresses(self):
        cPrint("")
        cPrint("Current recipients on mailing list:")
        cPrint("-----------------------------------")
        if len(self.emailAddressesToReachOutTo) == 0:
            cPrint("You currently have no recipients!")
        else:
            for emailAddress in self.emailAddressesToReachOutTo:
                cPrint("+  {}".format(emailAddress))

    def addEmailAddress(self):
        emailAddress = None
        if debugMode:
            emailAddress = "spencer.comora@gmail.com"
        else:
            emailAddress = str(input("<corona> Enter an email address to add: "))
        self.emailAddressesToReachOutTo.append(emailAddress)

    def sendNotification(self, notification):

        print("+---------------------+")
        print("| message length = {}|".format(len(notification)))
        print("+---------------------+")

        # can handle the entire array
        self.Session.sendMessageToContacts(self.emailAddressesToReachOutTo, notification)

    def refreshPopulations(self):
        countryPopulationScraper.updatePops(self)
    """
    staleStat, newStat
    """

    def updateAllCountries(self):
        timeBeforeCompleteUpdate = datetime.now()
        cPrint("Beginning to update all countries. . . timestamp: {}".format(str(timeBeforeCompleteUpdate)))

        # -------------------------------------------------------------------------------------
        notificationEnd = """
                            </ul>
                            </body>
                            </html>
                            """
        index = 0
        """
        General methodology
        for each country
            1.  grab its current statistics
            2.  update its statistics
                a.  make a call to virusTrackerAPIHandler with country's code
                b.  parse the response
                c.  call updateStats()
            3.  grab its new stats
            4.  compare the stats
                for each stat that meets its associated requirement
                    prepend its information to the message body
                
        """
        notification = ""
        if not self.isAPIDown():
            for country in self.countries:
                timeBeforeUpdate = datetime.now()
                cPrint("Updating {} statistics...".format(country.getCountryName()))

                # grab its current/stale statistics
                staleStatistics = country.getCurrentStatistics()

                # update its statistics
                country.updateCountry()

                notification += self.performAnalysisOnAllCountries()



                timeAfterUpdate = datetime.now()
                elapsedUpdateTime = timeAfterUpdate - timeBeforeUpdate
                cPrint(">>> {}'s statistics updated. Elapsed time: {}".format(country.getCountryName(), elapsedUpdateTime))

            # we have all the data for the day. now send it to everyone
            notificationWasSent = False
            if notification is not "":
                notificationWasSent = True
                notification = "".join([notificationHeader, notification, notificationEnd])
                self.sendNotification(notification)
                cPrint(">>> Just sent a notification to {} recipients."
                       .format(str(len(self.emailAddressesToReachOutTo))))
            else:
                cPrint(">>> No notification was sent. It's eerily quiet...")
                time.sleep(5)

            timeAfterCompleteUpdate = datetime.now()
            elapsedCompleteUpdateTime = timeAfterCompleteUpdate - timeBeforeCompleteUpdate
            cPrint("**********************************")
            cPrint("All countries updated!")
            cPrint("Elapsed time:\t{}".format(elapsedCompleteUpdateTime))
            if notificationWasSent:
                cPrint("NOTE: a notification was just sent!")
            cPrint("**********************************")

    def performAnalysisOnAllCountries(self):
        """
        Performs statistical analysis on all countries, accumulating
        the data into an html message along the way
        :return:
        """
        ret = ""
        for country in self.countries:
            ret += country.performStatisticalAnalysis()
        return ret


def cPrint(outStr):
    if outStr == "":
        print("")
    else:
        print(" ".join(["<corona>", str(datetime.now()), str(outStr)]))


availableStats = ["total_cases",
                  "total_recovered",
                  "total_unresolved",
                  "total_deaths",
                  "total_new_cases_today",
                  "total_new_deaths_today",
                  "total_active_cases",
                  "total_serious_cases"]


class CountryStatistic:
    def __init__(self, name):
        self.name = name
        self.data = 0  # TODO: rename to currData and move to below preChange
        self.prevData = 0
        self.prevChange = 0
        self.currChange = 0
        self.lastUpdateTime = datetime.now()  # TODO: need to call this somewhere?
        self.history = []

    def setPreviousData(self, previousData):
        self.previousData = previousData

    def getPreviousData(self):
        return self.previousData

    def setCurrentValue(self, currentValue):
        """
        wrapper for setStatisticValue for syntactic purposes
        """
        self.setStatisticValue(currentValue)

    def getPreviousChange(self):
        return self.prevChange

    def setPreviousChange(self, prevChange):
        """
        The new
        :param newData:
        :return:
        """
        self.prevChange = prevChange

    def getCurrentChange(self):
        return self.currChange

    def setCurrentChange(self, newData):

        self.currChange = newData - self.getCurrentValue()

    def updateStatistic(self, newData):
        """
        consider the updating of a country. the moment before:
        +   we have the moment before's prevData and currData
            +   thus we have the moment before's currChange = currData - prevData
        during/after update (we are holding newData as a parameter currently):
        +   prevChange becomes currChange
        +   currChange becomes new val - currVal
        then we update the values of newVal and currVal
        +   prevVal becomes currVal
        +   currVal becomes newData
        :param newData: incoming data
        :return:
        """
        # prevChange becomes currChange
        self.setPreviousChange(self.getPreviousChange())
        # currChange becomes newVal - currVal
        self.setCurrentChange(newData)

        # prevVal becomes currVal
        self.setPreviousData(self.getStatisticValue())  # set the previous data to the current data
        # currVal becomes newData
        self.setCurrentValue(newData)  # set the current data equal to the new data

    def isStatIncreasing(self):
        return self.getCurrentValue() > self.getPreviousData()

    def getCurrentValue(self):
        """
        wrapper for getStatisticValue for syntactic purposes
        :return: statistic's current value
        """
        return self.getStatisticValue()

    def getLastUpdateTime(self):
        return self.lastUpdateTime

    def setLastUpdateTime(self, lastUpdateTime):
        self.lastUpdateTime = lastUpdateTime

    def setLastUpdateTimeToNow(self):
        self.setLastUpdateTime(datetime.now())

    def getStatisticValue(self):
        return self.data

    def setStatisticValue(self, value):
        self.data = value

    def getStatisticName(self):
        return self.name

    def isStatSubsiding(self):
        return self.getCurrentChange() < self.getPreviousChange()

    def currOverPrev(self, curr, prev):
        try:
            return curr / prev
        except ZeroDivisionError:
            return 37

    def alarminglyBigChange(self):
        return False
        #return self.currOverPrev(self.getCurrentChange(), self.getPreviousChange()) > 2

    def percentageOfPopulation(self):
        """
        Reserved for future use
        """
        # TODO: implement this
        pass

    def checkAllConditions(self, countryName):
        """
        checks all depending on name
        :return: message to send
                externally... if message to send is returned as None don't send a message
                otherwise send one with message contents
        """
        output = ""
        if self.isStatSubsiding():
            output += "<li>{}'s {} are subsiding!".format(countryName, attrToStr(self.getStatisticName()))
            output += """
                            <ul>
                                <li>Previous change: {}</li>
                                <li>Current change: {}</li>
                                <li>Difference between changes: {}<li>
                            <ul>                
                        """.format(self.getPreviousChange(),
                                   self.getCurrentChange(),
                                   self.getCurrentChange() - self.getPreviousChange())
            output += "</li>\n"

        if self.alarminglyBigChange():
            output += "<li>The change in {}'s {} has more than doubled!".format(countryName,
                                                                                attrToStr(self.getStatisticName()))
            output += """
                            <ul>
                                <li>Previous change: {}</li>
                                <li>Current change: {}</li>
                                <li>Difference between changes: {}<li>
                                <li>Percent increase: {}</li>
                            <ul>                
                      """.format(self.getPreviousChange(),
                                 self.getCurrentChange(),
                                 self.getCurrentChange() - self.getPreviousChange(),
                                 str(
                                     self.currOverPrev(self.getCurrentChange(), self.getPreviousChange()) * 100))  # TODO: move this to helper fxn?
            output += "</li>\n"

        if self.percentageOfPopulation():
            """
            Reserved for future use
            """
            # TODO: implement this
            pass

        return output
    """
        Things to analyze:
        ------------------------------------------
    +   if a country's cases are subsiding
    +   if there's a significant change compared 
        to the last (maybe store prev/curr diffs?) 
    +   if a country's deaths surpass {X}
    +   
    """
    availableStats = ["total_cases",
                      "total_recovered",
                      "total_unresolved",
                      "total_deaths",
                      "total_new_cases_today",
                      "total_new_deaths_today",
                      "total_active_cases",
                      "total_serious_cases"]


class StatisticGroup:
    def __init__(self):
        self.allStats = []
        for stat in availableStats:
            # make a new country statistic with the
            # same name as the attribute
            newStat = CountryStatistic(stat)
            self.allStats.append(newStat)

    def searchStatistic(self, attribute):
        """
        :param attribute: statistic attribute to search for
        :return:    statistic being searched for (if input was valid)
                    None (if input was invalid)
        """
        for stat in self.allStats:
            if stat.getStatisticName() == attribute:
                return stat
        return None

    def getStatisticInGroup(self, attribute):
        """
        returns a statistic from the statistic group with given attribute
        :returns    foundStat   if the statistic could be found
                    -1          if the statistic could not be found
        """
        ret = -1
        foundStat = self.searchStatistic(attribute)
        if foundStat is not None:
            ret = foundStat
        return ret

    def setStatisticInGroup(self, attribute, value):
        """
        :param attribute: attribute to set
        :param value:     value to set attribute to
        """

        # get the statistic with given attribute
        self.searchStatistic(attribute) \
            .setStatisticValue(value)  # set the statistic's value


class Country(CoronaTexts):
    def __init__(self, countryName, countryCode):
        super().__init__()
        self.country_name = countryName
        self.country_code = countryCode
        self.country_stats = StatisticGroup()
        self.population = 0 # keep population member separate since separate refresh API
        self.timeStamp = datetime.now()

    def setPopulation(self, population):
        self.population = population

    def getPopulation(self):
        return self.population


    def getCurrentStatistics(self):
        return self.country_stats

    def updateCountry(self):
        """
        a.  make a call to virusTrackerAPIHandler with country's code
        b.  parse the response
        :return:    false if the API is down
                    true if the stats are all updated
        """
        if self.isAPIDown():
            return False
        # see what fetchCountryStats returns
        newStats = VirusTrackerAPIHandler.fetchCountryStats(self.getCountryCode())
        if newStats.text.strip() == "back soon fixing":
            cPrint("The API is down. Cannot update country statistics at this time.")
        else:
            self.updateStats(newStats)

    def updateStats(self, newStats):
        """
        updates the country's statistics/totals to those specified in newStats
        :param newStats:    JSON object of country stats
        :return:
        """
        # for each statistic
        currentStats = self.country_stats

        for statistic in newStats:
            if not statistic == "info":
                # assign the value of newStats[something] to country_stats[something
                self.country_stats.setStatisticInGroup(statistic, newStats[statistic])

    def getCountryName(self):
        return self.country_name

    def getCountryCode(self):
        return self.country_code

    def getStat(self, attribute):
        return self.country_stats.getStatisticInGroup(attribute)

    def performStatisticalAnalysis(self):
        """
        Analyzes the changes in each statistic for this country
        since the last update, and adds the results into an html string

        :return: html string with statistical analysis results for this country

        General methodology:
        1.  Get the country's statistic group
            a.  for each statistic in the statistic group
                (vv implementation here vv)
                    check if the statistic meets required conditions
                        II) get the current time                # or member function
                        III)get the previous update time
                        IV) store time since last update
                        V)  get the statistic's current value
                        VI) get the statistic's previous value
                            for each condition
                            # make a stat condition handler
                            # members:
                                if current and previous meet condition
                                    if not "needtosendalertflag":
                                        make need to send alert flag true
                                    append the data to the notification



        """
        analysisResults = ""

        # 1.    Get the country's statistic group
        freshStatistics = self.getCurrentStatistics()
        # a.    for each statistic in the statistic group

        for statObj in freshStatistics.allStats:
            # checkAllConditions needs country name to insert into html msg
            analysisResults += statObj.checkAllConditions(self.getCountryName())
            pass

        return analysisResults


def parseCountryTotals(countryTotals, destCountryTotals):
    """

    :param countryTotals:       takes in country totals json object for a country and a reference to
                                a place to store them for comparison and update with current country values
    :param destCountryTotals:   reference to store totals
    :return:                    none
    """
    # for each attribute in destCountryTotals
    for statistic in destCountryTotals.stats:
        # set all attributes
        destCountryTotals.setStatistic(statistic, countryTotals[statistic])
    return


menuOptions = ["Add email address", "Show all recipient email addresses", "Delete a recipient email address"]


def printUsrInput(inputStr):
    cPrint("You entered:\t {}".format(inputStr))


def getUsrMenuInput():
    if debugMode:
        return 0
    usrInput = 0
    while True:
        try:
            usrInput = int(input("<corona>\tEnter an option [0-6]:\t"))
        except ValueError:
            print("ERROR: Invalid input")
            continue
        if usrInput < 0 or usrInput > 6:
            print("ERROR: Input out of range!")
            printUsrInput(usrInput)
            continue
        else:
            break
    return usrInput


def printMenu():
    # we got here from a keyboard interrupt. need to clear to next line
    cPrint("")
    for menuOption in enumerate(menuOptions):
        cPrint("[{}]\t{}".format(menuOption[0], menuOption[1]))


def oneMinElapsedSince(sinceTime):
    now = datetime.now()
    if (now.second - sinceTime.second) >= 1:
        return True
    else:
        return False


# this controls how often to update all countries
elapseTimeInSeconds = helpers.daysToSeconds(1)

if debugMode:
    notificationTime = helpers.processHourAndMinuteAsString(
        ":".join([str(datetime.now().hour), str(datetime.now().minute)]))
else:
    notificationTime = helpers.processHourAndMinuteAsString("12:04")

# we initially do not need to send stats
needToSendStats = False


def hasTimeElapsed(updateTimer):
    """
    determines if updates should be sent, i.e. if the current HH:MM == update HH:MM
    :param updateTimer: a timer object to track one minute (to ensure that we don't
                        send updates at HH:MM, HH:MM+1 ...)
    :return: True       if updates should be sent
             False      if updates should not be sent
    """
    if debugMode:
        return True
    now = datetime.now()

    # if we loop back here within the same minute, we will
    # unintentionally send duplicates. start a timer for one
    # minute and don't send any while the timer is running

    # if timer is not running
    if updateTimer.isTimerDisabled():
        # we need to start the timer
        updateTimer.timerStart()
        # timer has not been started i.e. we are at the beginning
        # of the update minute. return true to trigger updates to
        # be sent in the main loop
        return True
    # if timer is running and has not overflowed
    elif updateTimer.isTimerRunning() and not updateTimer.hasTimerOverflowed():
        # return false so that we don't send notifications in the main loop
        return False
    # if one minute has passed
    elif updateTimer.hasTimerOverflowed():  # one minute has passed
        # disable the timer and return false so that we don't
        # send notifications in the main loop
        updateTimer.timerDisable()
        return False
    else:
        return False


def cPrintPollingAlert():
    os.system("clear")
    cPrint("+------------------------------------------------+")
    cPrint("|  CoronaTexts is currently polling for updates  |")
    cPrint("|  Press [Ctrl+C] to bring up the menu           |")
    cPrint("+------------------------------------------------+")


numMinsBetweenUpdates = 7


def main():
    coronaTexts = CoronaTexts()
    coronaTexts.constructCountries()  # 6 will be quit
    currTime = datetime.now()
    Session = Messaging.Session()
    Session.login()
    updateTimer = helpers.Timer(helpers.minutesToSeconds(numMinsBetweenUpdates))
    cPrintPollingAlert()

    while True:
        try:
            if hasTimeElapsed(updateTimer):
                # refresh all
                countryPopulationScraper.updatePops(coronaTexts)
                print("\t{}\t|\t{}\t".format("Name", "Population"))
                for country in coronaTexts.countries:
                    print("\t{}\t|\t{}\t".format(country.getCountryName(), int(country.getPopulation())))
                coronaTexts.updateAllCountries()
        except KeyboardInterrupt:
            printMenu()
            userInput = getUsrMenuInput()
            if userInput == 0:
                coronaTexts.addEmailAddress()
            if userInput == 1:
                coronaTexts.showAllEmailAddresses()
            cPrintPollingAlert()
        # if 1 minute has elapsed


if __name__ == '__main__':
    main()

# TODO: loop through all possible countries
#           store country code
#           create a country
