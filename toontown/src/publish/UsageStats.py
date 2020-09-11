
import sys
import time
import string
import re
import os
import shutil
import pprint
import math
import stats
from direct.showbase.PythonUtil import *

filterIps = ['^206\.16', '^206\.18']
filterIpsCompiled = map(re.compile, filterIps)

filterAccounts = ['^NeverSet',]
filterAccountsCompiled = map(re.compile, filterAccounts)

TABLE_ACCOUNT = 0
TABLE_TIME = 1
TABLE_LOGINS = 2

table = [[], [], []]

accounts = {}

signUps = {}
signUpsYearDict = {}
yearDict = {}

sessions = []
firstSessions = []
onlySessions = []

simDict = {}

toon27Offset = 12867601.0


fileName = "usage.txt"
print ("Opening %s" % fileName)
file = open(fileName)
# lines = file.readlines()
# print ("parsing %s lines" % len(lines))

LOG_FILENAME = 0
LOG_MSGTYPE = 1
LOG_CLIENTAGENT = 2
LOG_ACCOUNT = 3
LOG_END = 4
LOG_START = 5
LOG_IP = 6
LOG_NUMCOLUMNS = 12



def addOneInDict(dict, key):
    """
    If dict has key, return the value, otherwise insert the newValue and return it
    """
    if dict.has_key(key):
        dict[key] += 1
    else:
        dict[key] = 1

def getHourString(t):
    hours = int(t / 3600.0)
    min = int(round((t % 3600) / 60.0))
    sec = int(round((t % 3600) % 60))
    return ("%s:%s:%s" % (hours, min, sec))

def getHours(t):
    hours = (t / 3600.0)
    return ("%s" % (hours))

def getHistogramString(hist, binStrFunc=None):
    data = hist[0]
    start = hist[1]
    stride = hist[2]
    str = ""
    for i in range(len(data)):
        datum = data[i]
        bin = start + (i+1) * stride
        if binStrFunc:
            bin = binStrFunc(bin)
        str += ("%s,%s\n" % (bin, datum))
    return str
    

def getDay(t):
    # gmtime returns a 9-tuple starting with (year, month, day...)
    return time.gmtime(t)[0:3]

def convertTime(s):
    """
    Convert a log-style time in the form 2002/01/19 23:57:50
    to a python style time object
    """
    year = int(s[0:4])
    month = int(s[5:7])
    day = int(s[8:10])
    hour = int(s[11:13])
    min = int(s[14:16])
    sec = int(s[17:19])
    t = time.mktime((year, month, day, hour, min, sec, 0, 1, -1))
    if (month < 9) and (year == 2002):
        # Offset for toon27
        # print "old t: ", time.ctime(t)
        t += 12867601.0
        # print "new t: ", time.ctime(t)
    return t
    

#for line in lines:
lineNum = 0
while 1:
    line = file.readline()
    lineNum += 1
    if (lineNum % 1000) == 0:
        print "Line: %s" % lineNum

    if not line:
        print "end of file"
        break
        
    data = line.split('|')

    if len(data) < LOG_NUMCOLUMNS:
        print ("Bad data, len=%s line=%s" % (len(data), line))
        continue
    elif len(data) > 14:
        print ("Bad data, len=%s line=%s" % (len(data), line))        
        continue        

    filtered = 0
    
    accountName = data[LOG_ACCOUNT]
    for ipRegex in filterAccountsCompiled:
        if re.match(ipRegex, accountName):
            filtered = 1
            break
    
    #ip = data[LOG_IP]
    #for ipRegex in filterIpsCompiled:
    #    if re.match(ipRegex, ip):
    #        filtered = 1
    #        break
        
    if filtered:
        # print ("Filtering account: %s ip: %s" % (accountName, ip))
        continue
    
    endTime = data[LOG_END]
    startTime = data[LOG_START]
    e = convertTime(endTime)
    s = convertTime(startTime)
    dt = e - s

    resolution = 600.0 # seconds
    e = e - e % resolution
    s = s - s % resolution

    for t in range(s, e, resolution):
        if simDict.has_key(t):
            simDict[t] += 1
        else:
            simDict[t] = 1

    year, month, day = getDay(e)
    monthDict = yearDict.setdefault(year, {})
    dayDict = monthDict.setdefault(month, {})
    dayList = dayDict.setdefault(day, [])
    dayList.append(dt)

    sessions.append(dt)

    # Track the first time each account logged in
    firstLogin = signUps.get(accountName)
    if firstLogin:
        if s < firstLogin:
            signUps[accountName] = s
    else:
        signUps[accountName] = s
        # Record this first session for this account
        firstSessions.append(dt)
        
    
    index = accounts.get(accountName)
    if index:
        table[TABLE_TIME][index] += dt
        table[TABLE_LOGINS][index] += 1
    else:
        table[TABLE_ACCOUNT].append(accountName)
        table[TABLE_TIME].append(dt)
        table[TABLE_LOGINS].append(1)
        # Store this users index in the dict
        accounts[accountName] = len(table[TABLE_ACCOUNT]) - 1


for accountName, startTime in signUps.items():
    year, month, day = getDay(startTime)
    monthDict = signUpsYearDict.setdefault(year, {})
    dayDict = monthDict.setdefault(month, {})
    dayList = dayDict.setdefault(day, [])
    dayList.append(accountName)

# Compute the people that only played once
for i in range(len(table[TABLE_LOGINS])):
    if table[TABLE_LOGINS][i] == 1:
        playTime = table[TABLE_TIME][i]
        onlySessions.append(playTime)

print
print ("ACCOUNTS")
print ("--------------------------------------------------")
print ("Number of accounts: %s" % (len(accounts)))

print
print ("HOURS OF PLAY")
print ("--------------------------------------------------")
print ("Total play time: %s" %
       getHourString(stats.sum(table[TABLE_TIME])))
print ("Largest play time for a single account: %s" %
       getHourString(max(table[TABLE_TIME])))
print ("Median total play time for all accounts: %s" %
       getHourString(stats.median(table[TABLE_TIME])))
print ("Macro Histogram play time: \n%s" %
       getHistogramString(stats.histogram(table[TABLE_TIME], 10, [0,100*3600]), getHourString))
print ("Micro Histogram play time: \n%s" %
       getHistogramString(stats.histogram(table[TABLE_TIME], 10, [0,10*3600]), getHourString))
print ("Pico Histogram play time: \n%s" %
       getHistogramString(stats.histogram(table[TABLE_TIME], 12, [0,1*3600]), getHourString))

print
print ("LOGINS")
print ("--------------------------------------------------")
print ("Total logins: %s" %
       stats.sum(table[TABLE_LOGINS]))
print ("Largest logins for a single account: %s" %
       max(table[TABLE_LOGINS]))
print ("Median number of logins for all accounts: %s" %
       stats.median(table[TABLE_LOGINS]))
print ("Macro Histogram logins: \n%s" %
       getHistogramString(stats.histogram(table[TABLE_LOGINS], 10, [0,100])))
print ("Micro Histogram logins: \n%s" %
       getHistogramString(stats.histogram(table[TABLE_LOGINS], 10, [0,10])))


print
print ("SESSIONS")
print ("--------------------------------------------------")
print ("Largest session length: %s" %
       getHourString(max(sessions)))
print ("Median session length: %s" %
       getHourString(stats.median(sessions)))
print ("Macro Histogram session length: \n%s" %
       getHistogramString(stats.histogram(sessions, 10, [0,10*3600]), getHourString))
print ("Micro Histogram session length: \n%s" %
       getHistogramString(stats.histogram(sessions, 12, [0,1*3600]), getHourString))


print
print ("FIRST SESSIONS")
print ("--------------------------------------------------")
print ("Largest first session length: %s" %
       getHourString(max(firstSessions)))
print ("Median first session length: %s" %
       getHourString(stats.median(firstSessions)))
print ("Macro Histogram first session length: \n%s" %
       getHistogramString(stats.histogram(firstSessions, 10, [0,10*3600]), getHourString))
print ("Micro Histogram first session length: \n%s" %
       getHistogramString(stats.histogram(firstSessions, 12, [0,1*3600]), getHourString))



print
print ("FIRST SESSIONS THAT ONLY PLAYED ONCE")
print ("--------------------------------------------------")
print ("Largest first session length: %s" %
       getHourString(max(onlySessions)))
print ("Median first session length: %s" %
       getHourString(stats.median(onlySessions)))
print ("Macro Histogram first session length: \n%s" %
       getHistogramString(stats.histogram(onlySessions, 10, [0,10*3600]), getHourString))
print ("Micro Histogram first session length: \n%s" %
       getHistogramString(stats.histogram(onlySessions, 12, [0,1*3600]), getHourString))


print
print ("Dailies")
print ("Sum of play per day: \n")
for year, monthDict in yearDict.items():
    for month, dayDict in monthDict.items():
        for day, dayList in dayDict.items():
            print ("%s-%s-%s, %s" % (year, month, day, getHours(stats.sum(dayList))))
print
print ("Median session length per day: \n")
for year, monthDict in yearDict.items():
    for month, dayDict in monthDict.items():
        for day, dayList in dayDict.items():
            print ("%s-%s-%s, %s" % (year, month, day, getHourString(stats.median(dayList))))

print
print ("Logins per day: \n")
for year, monthDict in yearDict.items():
    for month, dayDict in monthDict.items():
        for day, dayList in dayDict.items():
            print ("%s-%s-%s, %s" % (year, month, day, len(dayList)))

print
print ("Signups per day: \n")
for year, monthDict in signUpsYearDict.items():
    for month, dayDict in monthDict.items():
        for day, dayList in dayDict.items():
            print ("%s-%s-%s, %s" % (year, month, day, len(dayList)))

print
print ("Simutaneous users\n")
print ("Most simultanous users: %s\n" % (max(simDict.values())))
