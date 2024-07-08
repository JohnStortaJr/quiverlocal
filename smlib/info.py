#!/usr/bin/python3

from smlib.core import *
from smlib.format import *
import json

def getSiteList(localDatabase="./sitedb"):
    keepRunning = True

    while keepRunning:
        os.system('clear')
        menuCounter = 0
        print(6 * "-" , "Installed Sites" , 6 * "-")

        siteList = os.listdir(localDatabase)

        for i in siteList:
            menuCounter += 1
            print(style.BOLD + str(menuCounter) + " " + style.END + i)

        print("")
        print(style.BOLD + "0 " + style.END + "Back")    
        print(21 * "-")

        selection = int(input("Enter option [0-" + str(menuCounter) + "]: "))

        if selection > len(siteList):
            continue
        elif selection == 0:
            return
        
        readSiteConfig(siteList[selection-1])
        input("Hit ENTER to Continue")










def readSiteConfig(siteName, quiverHome=os.getcwd()):
    # Open JSON file named site.Name.json in the configdb directory
    # Read the contents into a dictionary
    fileName = quiverHome + "/sitedb/" + siteName
    print(fileName)

    with open(fileName, 'r') as inFile:
        activeSite = json.load(inFile)

    # Print the dictionary
    print(json.dumps(activeSite, indent=4, sort_keys=True))
    #print(activeSite)
    return activeSite

def writeSiteConfig(siteName, siteDictionary, quiverHome=os.getcwd()):
    # Open JSON file named siteName.json in the configdb directory
    # Write the contents of the activeSite dictionary to the file
    with open(quiverHome + "/sitedb/" + siteName + ".json", 'w') as outFile:
        json.dump(siteDictionary, outFile, indent=4)
        outFile.write("\n")

