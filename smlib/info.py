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

        for i in siteFileList:
            menuCounter += 1

            if i.endswith(".json"):
                with open(quiverDB + i, 'r') as inFile:
                    currentSite = json.load(inFile)
                    siteList.append(currentSite["siteName"])
                    print(style.BOLD + str(menuCounter) + " " + style.END + currentSite["siteName"])

        print("")
        print(style.BOLD + "0 " + style.END + "Back")    
        print(21 * "-")

        selection = int(getInput("Which site details do you wish to see [0-" + str(menuCounter) + "]? ", True))

        if selection > len(siteList):
            print(background.BCYAN + "Unknown selection" + background.END)
            continue
        elif selection == 0:
            return
        
        displaySiteConfig(siteList[selection-1])
        input("Hit ENTER to Continue")



# Open JSON file named siteName.json in the sitedb directory
# and return a dictionary with the contents
def readSiteConfig(siteName):
    with open(quiverDB + siteName + ".json", 'r') as inFile:
        return json.load(inFile)

# Display the contents of the siteName.json file for the indicated site
def displaySiteConfig(siteName): 
    print(style.BOLD + "Site details for: " + style.END + siteName)
    print(json.dumps(readSiteConfig(siteName), indent=4))

# Write the provided dictionary to siteName.json in sitedb (overwriting any existing values)
def writeSiteConfig(siteDictionary):
    with open(quiverDB + siteDictionary["siteName"] + ".json", 'w') as outFile:
        json.dump(siteDictionary, outFile, indent=4)
        outFile.write("\n")


def deleteSite():
    #### Add warnings and prompts before deleting
    targetSite = readSiteConfig(getInput("Which site do you wish to delete ? "))

    print(json.dumps(targetSite, indent=4))

    # disable the site in apache
    runCommand("a2dissite " + targetSite["siteName"], True)

    # restart apache
    restartApache()

    # Delete the apache config files
    runCommand("rm " + targetSite["domainConfig"])
    runCommand("rm " + targetSite["apacheConfig"], True)

    # Delete the domain directory
    runCommand("rm -rf " + targetSite["domainHome"])

    # drop the database
    runCommand("mysql -u root -e 'DROP DATABASE " + targetSite["dbName"] + ";'", True)

    # delete the config json file
    runCommand("rm " + quiverHome + "/sitedb/" + targetSite["siteName"] + ".json")
