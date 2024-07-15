#!/usr/bin/python3

from smlib.core import *
from smlib.format import *
import json

def getSiteList(localDatabase = quiverDB):
    keepRunning = True

    while keepRunning:
        #os.system('clear')
        print("")
        menuCounter = 0
        print(6 * "-" , "Installed Sites" , 6 * "-")

        siteFileList = sorted(os.listdir(localDatabase))
        siteList = []
        trustedList = []

        for i in siteFileList:
            menuCounter += 1

            if i.endswith(".json"):
                with open(quiverDB + i, 'r') as inFile:
                    currentSite = json.load(inFile)
                    siteList.append(currentSite["siteName"])
                    trustedList.append(currentSite["isTrusted"])
                    if currentSite["isTrusted"]:
                        trustMark = " ♥"
                    else:
                        trustMark = ""

                    print(style.NEGATIVE + str(menuCounter) + style.END + " " + currentSite["siteName"] + color.BBLUE + trustMark + style.END)

        print("")
        print(style.NEGATIVE + "0" + style.END + " Back")    
        print(21 * "-")

        selection = int(getInput("Which site details do you wish to see [0-" + str(menuCounter) + "]? ", True))

        if selection > len(siteList):
            print(background.BYELLOW + "Unknown selection" + background.END)
            continue
        elif selection == 0:
            return
        
        displaySiteConfig(siteList[selection-1])
        input("Hit ENTER to Continue")


def getTablePrefixes():

    print("")
    menuCounter = 0
    print(6 * "-" , "Installed Sites" , 6 * "-")

    siteFileList = sorted(os.listdir(quiverDB))
    siteList = []

    for i in siteFileList:
        menuCounter += 1

        if i.endswith(".json"):
            with open(quiverDB + i, 'r') as inFile:
                foundSite = json.load(inFile)
                siteList.append(foundSite)
                tablePrefix = runCommand("awk '/table_prefix/{print $3}' " + foundSite["domainHome"] + "/wp-config.php")[1:-3]
                print(foundSite["siteName"] + ">> " + tablePrefix)


def updateTablePrefix(targetSite):
    targetSite["tablePrefix"] = runCommand("awk '/table_prefix/{print $3}' " + targetSite["domainHome"] + "/wp-config.php")[1:-3]
    writeSiteConfig(targetSite)


def isUnique(key, value):
    # Get list of config files
    siteFileList = sorted(os.listdir(quiverDB))

    # Open each config file (end with json)
    for i in siteFileList:

        if i.endswith(".json"):

            with open(quiverDB + i, 'r') as inFile:
                existingSite = json.load(inFile)

                # If the existing config for the given key matches the provided value, then this entry is a duplicate
                if existingSite[key] == value:
                    return False
    
    return True


### Open JSON file named siteName.json in the sitedb directory
### and return a dictionary with the contents
def readSiteConfig(siteName):
    with open(quiverDB + siteName + ".json", 'r') as inFile:
        return json.load(inFile)


### Display the contents of the siteName.json file for the indicated site
def displaySiteConfig(siteName): 
    print(style.BOLD + "Site details for: " + style.END + siteName)
    print(json.dumps(readSiteConfig(siteName), indent=4))


### Write the provided dictionary to siteName.json in sitedb (overwriting any existing values)
def writeSiteConfig(siteDictionary):
    with open(quiverDB + siteDictionary["siteName"] + ".json", 'w') as outFile:
        json.dump(siteDictionary, outFile, indent=4)
        outFile.write("\n")
