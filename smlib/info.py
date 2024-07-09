#!/usr/bin/python3

from smlib.core import *
from smlib.format import *
import json

def getSiteList(localDatabase = quiverDB):
    keepRunning = True

    while keepRunning:
        os.system('clear')
        menuCounter = 0
        print(6 * "-" , "Installed Sites" , 6 * "-")

        siteList = sorted(os.listdir(localDatabase))

        for i in siteList:
            menuCounter += 1

            if i.endswith(".json"):
                with open(quiverDB + i, 'r') as inFile:
                    currentSite = json.load(inFile)
                    print(style.BOLD + str(menuCounter) + " " + style.END + currentSite["site_name"])

        print("")
        print(style.BOLD + "0 " + style.END + "Back")    
        print(21 * "-")

        selection = int(input("Enter option [0-" + str(menuCounter) + "]: "))

        if selection > len(siteList):
            continue
        elif selection == 0:
            return
        
        displaySiteConfig(siteList[selection-1])
        input("Hit ENTER to Continue")



# Open JSON file named siteName.json in the sitedb directory
# and return a dictionary with the contents
def readSiteConfig(siteName):
    with open(quiverDB + siteName, 'r') as inFile:
        activeSite = json.load(inFile)
    
    return activeSite

# Display the contents of the siteName.json file for the indicated site
def displaySiteConfig(siteName): 
    print(style.BOLD + "Site details for: " + style.END + siteName)
    print(json.dumps(readSiteConfig(siteName), indent=4))

# Write the provided dictionary to siteName.json in sitedb (overwriting any existing values)
def writeSiteConfig(siteDictionary):
    with open(quiverDB + siteDictionary["site"]["name"] + ".json", 'w') as outFile:
        json.dump(siteDictionary, outFile, indent=4)
        outFile.write("\n")

