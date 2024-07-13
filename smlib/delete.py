#!/usr/bin/python3

from smlib.core import *
from smlib.format import *
import json

def deleteSite(localDatabase = quiverDB):
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
                    foundSite = json.load(inFile)
                    siteList.append(foundSite)

                    if foundSite["isTrusted"]:
                        print(style.NEGATIVE + str(menuCounter) + style.END + " " + foundSite["siteName"] + color.BBLUE +  " ♥" + color.END)
                    else:
                        print(style.NEGATIVE + str(menuCounter) + style.END + " " + foundSite["siteName"] + style.END )

        print("")
        print(style.NEGATIVE + "0" + style.END + " Back")    
        print(21 * "-")

        selection = int(getInput("Which site would you like to delete [0-" + str(menuCounter) + "]? ", True))

        if selection > len(siteList):
            print(background.BYELLOW + "Unknown selection" + background.END)
            continue
        elif selection == 0:
            return
        
        # Display the selected site details and get confirmation before proceeding
        print(json.dumps(siteList[selection-1], indent=4))
        print("")
        confirmationCount = 0
        confirmation = input(style.BOLD + "Are you sure you wish to delete this site [y/N]? " + style.END).strip()
        if confirmation == "y" or confirmation == "Y":
            confirmationCount += 1
            confirmation = input(background.BMAGENTA + "There is no turning back. " + background.END + "\n" + style.BOLD + "Are you certain you wish to " + style.END + style.BLINK + "permanently" + style.END + style.BOLD + " delete this site [y/N]? " + style.END).strip()
            if confirmation == "y" or confirmation == "Y":
                confirmationCount += 1

        if confirmationCount < 2:
            # Insufficient confirmations. Return without taking any action.
            print("")
            print(background.BYELLOW + "Site deletion aborted!" + background.END + style.ITALIC + " (no changes made)" + style.END)

            continue

        deleteSiteConfiguration(siteList[selection-1])

        print("")
        print(style.BOLD + siteList[selection-1]["siteName"] + style.END + " has been permanently deleted " + style.END)
        print("")



def deleteSiteConfiguration(targetSite):
    # Disable the site in apache
    runCommand("a2dissite " + targetSite["siteName"], True)

    # Restart apache
    restartApache()

    # Delete the config files
    runCommand("rm " + targetSite["domainConfig"])
    runCommand("rm " + targetSite["apacheConfig"], True)

    # Delete the domain directory
    runCommand("rm -rf " + targetSite["domainHome"])

    # Delete the database
    runCommand("mysql -u root -e 'DROP DATABASE " + targetSite["dbName"] + ";'", True)

    # Delete the sitedb json file
    runCommand("rm " + quiverHome + "/sitedb/" + targetSite["siteName"] + ".json")
