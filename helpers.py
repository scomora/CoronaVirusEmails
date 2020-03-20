"""
:param date - receives string of form MMDDYYYY and returns date obj
"""
import time
from datetime import date
import datetime
import re
from enum import Enum


# TODO: add menuOptions here

def parseDate(date):
    month = int(date[0:2])
    day = int(date[2:4])
    year = int(date[4:8])

    return year, month, day


def parseTime(timeStr):
    timeStr = timeStr.split(":")
    hour = int(timeStr[0])
    minute = int(timeStr[1])

    return hour, minute


def daysToSeconds(days):
    return 24 * hoursToSeconds(days)


def hoursToSeconds(hours):
    return 60 * minutesToSeconds(hours)


def minutesToSeconds(minutes):
    return 60 * minutes


def mapCarrierAbbreviationToEmailExtension(carrierAbbreviation):
    if carrierAbbreviation == 'A':
        return destinationAddressDict["AT&T"]
    elif carrierAbbreviation == 'V':
        return destinationAddressDict["Verizon"]
    elif carrierAbbreviation == 'T':
        return destinationAddressDict["TMobile"]


"""
userInput is string in form of <num> <unit>
where unit can be days, hours, minutes, or seconds
"""


def processRemindTime(remindFrequencyString):
    frequency = int(remindFrequencyString.split(' ')[0])
    timeUnit = remindFrequencyString.split(' ')[1]

    if timeUnit == 'd':
        return daysToSeconds(frequency)
    elif timeUnit == 'h':
        return hoursToSeconds(frequency)
    elif timeUnit == 'm':
        return minutesToSeconds(frequency)
    elif timeUnit == 's':
        return frequency


def hasNumbers(inputStr):
    return any(char.isdigit() for char in inputStr)


def hasLetters(inputStr):
    for char in inputStr:
        if char.isalpha():
            return True
    return False


def getUserRemindFrequency():
    usrRemindFreq = None
    while True:
        try:
            usrRemindFreq = str(input("Enter how often to receive reminders in a day <num> <h, m, s>: "))
        except ValueError:
            print("ERROR: Something went wrong. I didn't catch that.\n")
            continue
        if len(usrRemindFreq) <= 0 or usrRemindFreq is None:
            print("ERROR: Reminder frequency cannot be empty!\n")

        # if there's no number in the user's input
        else:
            if not hasNumbers(usrRemindFreq):
                print("Your input for the requested remind frequency does not contain any numbers!")
                continue
            elif not hasLetters(usrRemindFreq):
                print("Your input for the requested remind frequency does not contain any letters!")
                continue
            else:
                break
    return usrRemindFreq


def getAndProcessRemindFrequency():
    """
    processes user input for remind frequency until valid input received
    then parses it and converts it to seconds
    @return remind frequency in seconds
    """
    remindFrequency = getUserRemindFrequency()
    remindFrequencyInSeconds = processRemindTime(remindFrequency)
    return remindFrequencyInSeconds


def processDate(dateAsString):
    """
    @param  dateAsString:   expects input in form of MM/DD/YYYY
    @return date object representing the provided MMDDYYYY
    """
    month = int(dateAsString.split('/')[0])
    day = int(dateAsString.split('/')[1])
    year = int(dateAsString.split('/')[2])

    return datetime.date(year, month, day)


def containsBackslashes(inputStr):
    if inputStr.find("/") != -1:
        return True
    else:
        return False


def getNumBackslashes(inputStr):
    numBackslashes = 0
    for char in inputStr:
        if char == '/':
            numBackslashes += 1
    return numBackslashes


def monthOutOfBounds(month):
    if month < 1 or month > 12:
        return True
    else:
        return False


def dayOutOfBounds(day):
    if day < 1 or day > 31:
        return True
    else:
        return False


def getAndProcessDate():
    usrDate = None
    while True:
        try:
            usrDate = str(input("Enter the last date on which you wish to receive "
                                "this reminder (<MMDDYYYY> or <MM/DD/YYYY>): "))
        except ValueError:
            print("ERROR: Something went wrong. I didn't catch that.\n")
            continue
        if len(usrDate) <= 0 or usrDate is None:
            print("ERROR: Date cannot be empty!\n")
            continue
        # if no backslashes (MMDDYYYY)
        elif not containsBackslashes(usrDate):
            if len(usrDate) != 6:
                print("ERROR: The date you entered does not contain"
                      "backslashes, but is not of the form MMDDYYYY. Please"
                      "Ensure that you are entering six [6] characters for the "
                      "date (ex: 09042020)")
                continue
            else:
                break
        # if only one backslash, invalid
        elif getNumBackslashes(usrDate) == 1:
            print("ERROR: The date you entered only contains one [1] backslash [/]."
                  "Please enter either two backslashes (using the form MM/DD/YYYY "
                  "or no backslash using the form MMDDYYYY.")
            continue
        else:
            # we can extract the MM DD YYYY
            month = int(usrDate.split("/")[0])
            day = int(usrDate.split("/")[1])
            year = int(usrDate.split("/")[2])
            if monthOutOfBounds(month):
                print("ERROR: Month out of bounds. Month must be between 1 and 12. "
                      "You entered: {}".format(month))
                continue
            elif dayOutOfBounds(day):
                print("ERROR: Day out of bounds. Day must be between 1 and 31. "
                      "You entered: {}".format(day))
            else:
                break
    return processDate(usrDate)


def processHourAndMinuteAsString(hourAndMinute):
    hour = int(hourAndMinute.split(':')[0])
    minute = int(hourAndMinute.split(':')[1])

    now = datetime.datetime.now()

    year = now.year
    month = now.month

    day = now.day
    second = 0

    return datetime.datetime(year, month, day, hour, minute, second)


def getUsrReminderDesc():
    usrReminderDesc = None
    while True:
        try:
            usrReminderDesc = str(input("Enter reminder description: "))
        except ValueError:
            print("ERROR: Something went wrong. I didn't catch that.\n")
            continue
        if len(usrReminderDesc) <= 0 or usrReminderDesc is None:
            print("ERROR: Reminder description cannot be empty!\n")
            continue
        else:
            break
    return usrReminderDesc


def containsColons(timeStr):
    """
    checks if string contains any colons
    @return True if string contains colons
            False otherwise
    """
    if timeStr.find(":") != -1:
        return True
    else:
        return False


def hourOutOfBounds(hour):
    """
    checks user input string if hour is out of bounds
    @return True if the hour is out of bounds (!(0 <= hr <= 23))
    """
    if hour < 0 or hour > 23:
        return True
    else:
        return False


def minuteOutOfBounds(minute):
    """
    checks user input string if minute is out of bounds
    @return True if the minute is out of bounds (!(0 <= minute <= 59))
    """
    if minute < 0 or minute > 59:
        return True
    else:
        return False


def getUsrTimeInput(prompt):
    """
    @param prompt:  prompt to display to user (depending
                    on start or end time)
    @return:        fully validated usrTimeInput
    """
    usrTimeInput = None
    while True:
        try:
            usrTimeInput = str(input(prompt))
        except ValueError:
            print("ERROR: Something went wrong. I didn't catch that.\n")
            continue
        if len(usrTimeInput) <= 0 or usrTimeInput is None:
            print("ERROR: Time cannot be empty!\n")
            continue
        elif not containsColons(usrTimeInput):
            print("ERROR: Time input must be in the form of <HH>:<MM>. "
                  "No colon found!\n")
            continue

        else:
            # if we're here, then we have HH:MM input. now parse the hour and minute
            hour = int(usrTimeInput.split(":")[0])
            minute = int(usrTimeInput.split(":")[1])

            if hourOutOfBounds(hour):
                print("The hour you entered is outside of the bounds of 0 and 23. You entered: {}".format(str(hour)))
                continue
            elif minuteOutOfBounds(minute):
                print(
                    "The minute you entered is outside of the bounds of 0 and 59. You entered: {}".format(str(minute)))
                continue
            else:
                break
    return usrTimeInput


class StartOrEndTime(Enum):
    START_TIME = 1
    END_TIME = 2


class FirstOrLastName(Enum):
    FIRST_NAME = 1
    LAST_NAME = 2


def getUsrContactName(prompt):
    usrContactNameInput = None
    while True:
        try:
            usrContactNameInput = str(input(prompt))
        except ValueError:
            print("ERROR: Something went wrong. I didn't catch that.\n")
            continue
        if len(usrContactNameInput) <= 0 or usrContactNameInput is None:
            print("ERROR: Name input cannot be empty!\n")
            continue
        else:
            break
    return usrContactNameInput


def getNumOfCharInString(charToFind, strToSearch):
    numInstancesOfChar = 0
    for char in strToSearch:
        if char == charToFind:
            numInstancesOfChar += 1
    return numInstancesOfChar


def getNumSpaces(inputStr):
    return getNumOfCharInString(" ", inputStr)


def getNumDashes(inputStr):
    return getNumOfCharInString("-", inputStr)


def getAndProcessTime(timeType):
    prompt = ""
    if timeType == StartOrEndTime.START_TIME:
        prompt = "Enter a time to begin receiving the reminder " \
                 "during the day (<HHMM>, 24-hour format): "
    elif timeType == StartOrEndTime.END_TIME:
        prompt = "Enter a time to last receive the reminder " \
                 "during the day (<HHMM>, 24-hour format): "

    usrTimeInput = getUsrTimeInput(prompt)

    usrTimeInput = processHourAndMinuteAsString(usrTimeInput)
    return usrTimeInput


def printHeader():
    pass


def formatUsrInput(usrInput):
    return "You entered:\t{}".format(usrInput)


def getAreaCodeNoSpaces(phoneNum):
    return phoneNum[0:3]


def getMiddleDigitsNoSpaces(phoneNum):
    return phoneNum[3:7]


def getLastFourDigitsNoSpaces(phoneNum):
    return phoneNum[7:10]


def getAreaCodeFromDelineator(phoneNum, delineator):
    if delineator is "":
        return getAreaCodeNoSpaces(phoneNum)  # first 3
    else:
        return phoneNum.split(delineator)[0]


def getMiddleDigitsFromDelineator(phoneNum, delineator):
    if delineator is "":
        return getMiddleDigitsNoSpaces(phoneNum)
    else:
        return phoneNum.split(delineator)[1]


def getLastFourDigitsFromDelineator(phoneNum, delineator):
    if delineator is "":
        return getLastFourDigitsNoSpaces(phoneNum)
    else:
        return phoneNum.split(delineator)[2]


class PhoneNumType(Enum):
    NO_SPACES = 1
    SPACES = 2
    DASHES = 3


def getContactPhoneNumber():
    usrContactPhoneNum = None
    areaCode = ""
    middleDigits = ""
    lastFourDigits = ""
    delineator = ""  # char that delineates the 10 dig phone number
    while True:
        try:
            usrContactPhoneNum = str(input("Enter 10-digit phone number "
                                           "(1112223333, 111 222 3333,"
                                           "111-222-3333"))
        except ValueError:
            print("ERROR: Something went wrong. I didn't catch that.\n")
            continue
        if len(usrContactPhoneNum) <= 0 or usrContactPhoneNum is None:
            print("ERROR: Phone number input cannot be empty!\n")
            continue
        # if no spaces
        if getNumSpaces(usrContactPhoneNum) == 0:
            # if not 10 digits
            if not len(usrContactPhoneNum) == 10:
                print("ERROR: Phone number not 10 digits!")
                print(formatUsrInput(usrContactPhoneNum))
            else:
                delineator = ""
                break
        # if spaces
        elif getNumSpaces(usrContactPhoneNum) > 0:
            # if only one space
            if getNumSpaces(usrContactPhoneNum) != 2:
                print("ERROR: Phone number contains incorrect number "
                      "of spaces! In order to use spaces, please"
                      "enter a phone number of the form"
                      "111 222 3333.")
                print(formatUsrInput(usrContactPhoneNum))
            else:
                delineator = " "
                break
        # if dashes
        elif getNumDashes(usrContactPhoneNum) > 0:
            # if not two dashes
            if getNumDashes(usrContactPhoneNum) != 2:
                print("ERROR: Phone number contains incorrect number "
                      "of dashes! In order to use spaces, please"
                      "enter a phone number of the form"
                      "111-222-3333.")
                print(formatUsrInput(usrContactPhoneNum))
            else:
                delineator = "-"
                break
        else:
            print("ERROR: Your input could not be validated.\n")
            continue

            # else if two spaces
    areaCode = getAreaCodeFromDelineator(usrContactPhoneNum, delineator)
    middleDigits = getMiddleDigitsFromDelineator(usrContactPhoneNum, delineator)
    lastFourDigits = getLastFourDigitsFromDelineator(usrContactPhoneNum, delineator)

    # return the concatenation of the above
    return


def getAndProcessName(nameType):
    """
    @param  nameType:   first or last name for generation of
                        input prompt
    @return             fully validated user name (can be first
                        or last)
    """
    prompt = ""
    firstOrLast = ""
    if nameType == FirstOrLastName.FIRST_NAME:
        firstOrLast = "first"
    elif nameType == FirstOrLastName.LAST_NAME:
        firstOrLast = "last"
    prompt = "Enter contact {} name".format(firstOrLast)
    return getUsrContactName(prompt)


def printMenu():
    i = 0

    # to separate first menu option from
    # keyboard interrupt keystroke
    print("\n")
    for menuOption in menuOptions.keys():
        print(menuOption + ":\t" + menuOptions[menuOption])

def getPercentIncrease(old, new):
    try:
        return 100 * new / old
    except ZeroDivisionError:
        return 0


def quit():
    # every time curr time's secs is multiple of 2
    print("Quitting ")
    for i in range(3):
        time.sleep(1)
        print(". ")


destinationAddressDict = {
    "AT&T": "@txt.att.net",
    "TMobile": "@tmomail.net",
    "Verizon": "@vzwpix.com"
}

menuOptions = {
    "n": "Quit this session and begin a new one",
    "d": "Show destination addresses",
    "r": "Set a reminder",
    "s": "Send a text",
    "m": "Manually service reminders"
}

class TimerState(Enum):
    TIMER_ENABLED = 1,
    TIMER_RUNNING = 2,
    TIMER_OVERFLOWED_WAITING_RESET = 3,
    TIMER_DISABLED = 4

class Timer:
    """
    timer that you can use by polling
    timer = Timer(60)   # timer for 1 min
    timer.startTimer()  # start the timer
    while not timer.hasTimerOverflowed():
        # do stuff
    # timer overflowed. do stuff that needs to be done after timer overflows
    timer.restart()
    """

    def __init__(self, perInSecs):
        """
        :param perInSecs: period in seconds for the timer
        """
        self.lastOverflowTime = 0
        self.per = perInSecs
        self.state = TimerState.TIMER_DISABLED

    def setPer(self, perInSecs):
        self.per = perInSecs

    def getPer(self):
        return self.per

    def getPerAsTimeDelta(self):
        return datetime.timedelta(seconds=self.getPer())

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def isTimerDisabled(self):
        return self.getState() == TimerState.TIMER_DISABLED

    def isTimerRunning(self):
        return self.getState() == TimerState.TIMER_RUNNING

    def setLastOverflowTime(self, time):
        self.lastOverflowTime = time

    def getLastOverflowTime(self):
        return self.lastOverflowTime

    def resetLastOverflowTime(self):
        self.setLastOverflowTime(datetime.datetime.now())


    def timerRestart(self):
        self.timerStart()

    def timerStart(self):
        self.resetLastOverflowTime()
        self.setState(TimerState.TIMER_RUNNING)

    def timerDisable(self):
        self.setState(TimerState.TIMER_DISABLED)

    def hasTimerOverflowed(self):
        # if last time plus timedelta for overflow is now
        return (self.getLastOverflowTime() + self.getPerAsTimeDelta()) >= datetime.datetime.now()

