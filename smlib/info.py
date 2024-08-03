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

        siteFileList = sorted(os.listdir(localDatabase + "/sites"))
        siteList = []
        trustedList = []

        for i in siteFileList:
            menuCounter += 1

            if i.endswith(".json"):
                with open(quiverDB + "/sites/" + i, 'r') as inFile:
                    currentSite = json.load(inFile)
                    siteList.append(currentSite["siteName"])
                    trustedList.append(currentSite["isTrusted"])
                    if currentSite["isTrusted"]:
                        trustMark = " ♥"
                    else:
                        trustMark = ""

                    print(style.NEGATIVE + str(menuCounter) + style.END + " " + currentSite["siteName"] + color.BBLUE + trustMark + style.END)

        print("")

        if menuCounter == 0:
            print(background.BYELLOW + " No sites found " + background.END)
            print(21 * "-")
            selection = getInput("Hit " + style.BOLD + "Enter" + style.END + " to return to main menu... ")
            return
        else:
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



def updateTablePrefix(targetSite):
    with open(targetSite["domainHome"] + "/wp-config.php", 'r') as inFile:
        # Read all lines form the file into a list
        configLines = inFile.readlines()

        # Check each line until finding table_prefix and then return that value
        for i in configLines:
            if "table_prefix" in i:
                foundLine = i
                break

    targetSite["tablePrefix"] = foundLine.split("=")[1][2:-4]
    writeSiteConfig(targetSite)


def isUnique(key, value):
    # Get list of config files
    siteFileList = sorted(os.listdir(quiverDB + "/sites"))

    # Open each config file (end with json)
    for i in siteFileList:

        if i.endswith(".json"):

            with open(quiverDB + "/sites/" + i, 'r') as inFile:
                existingSite = json.load(inFile)

                # If the existing config for the given key matches the provided value, then this entry is a duplicate
                if existingSite[key] == value:
                    return False
    
    return True


### Open JSON file named siteName.json in the sitedb directory
### and return a dictionary with the contents
def readSiteConfig(siteName):
    with open(quiverDB + "/sites/" + siteName + ".json", 'r') as inFile:
        return json.load(inFile)


### Display the contents of the siteName.json file for the indicated site
def displaySiteConfig(siteName): 
    print(style.BOLD + "Site details for: " + style.END + siteName)
    print(json.dumps(readSiteConfig(siteName), indent=4))


### Write the provided dictionary to siteName.json in sitedb (overwriting any existing values)
def writeSiteConfig(siteDictionary):
    with open(quiverDB + "/sites/" + siteDictionary["siteName"] + ".json", 'w') as outFile:
        json.dump(siteDictionary, outFile, indent=4)
        outFile.write("\n")
