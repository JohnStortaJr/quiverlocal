#!/usr/bin/python3

from smlib.core import *
from smlib.format import *
from smlib.info import *
from smlib.create import *
import json
import shutil

def trustSite(localDatabase = quiverDB):
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
                    updateTablePrefix(foundSite)

                    if foundSite["isTrusted"]:
                        print(style.FAINT + str(menuCounter) + " " + foundSite["siteName"] + " ♥" + style.END)
                    else:
                        print(style.BOLD + str(menuCounter) + " " + foundSite["siteName"] + style.END )

        print("")
        print(style.BOLD + "0 " + style.END + "Back")    
        print(21 * "-")

        selection = int(getInput("Which site would you like to trust [0-" + str(menuCounter) + "]? ", True))

        if selection > len(siteList):
            print(background.BYELLOW + "Unknown selection" + background.END)
            continue
        elif selection == 0:
            return
        
        if siteList[selection-1]["isTrusted"]:
            print(background.BYELLOW + siteList[selection-1]["siteName"] + " is already trusted" + background.END)
            confirmation = input("Do you wish to change the certificate used by this site [y/N]? ").strip()

            if (confirmation != "y") and (confirmation != "Y"): continue

        siteToTrust = siteList[selection-1].copy()
        #print(json.dumps(siteToTrust, indent=4))
        print("This will add an existing SSL certificate to the site. The signed certificates must already exist.")

        # Get the paths to the certificate files from the user
        siteToTrust = getCertificate(siteToTrust)

        # Add the certificate paths to the Apache configuration
        addCertificate(siteToTrust)

        # Update the WordPress database to reflect the https URLs
        updateSiteValues(siteToTrust, "https")

        restartApache()

        # Mark this site as trusted and write the dictionary to the quiver database
        siteToTrust["isTrusted"] = True
        writeSiteConfig(siteToTrust)

        print("")
        print(style.BOLD + siteToTrust["siteName"] + style.END + " is now trusted " + style.END)
        print("Once the corresponding CA ROOT certificate is added to the local system, ")
        print("the site can be accessed using https://" + siteToTrust["domainName"] + style.END)



def getCertificate(targetSite):
    # Default to the current certificate key file, if there is one. Otherwise, assume siteName.key
    defaultCertKeyFile = targetSite["certKey"]
    if not defaultCertKeyFile: defaultCertKeyFile = targetSite["userHome"] + "/certificates/" + targetSite["siteName"] + ".key"
    print(json.dumps(targetSite, indent=4))

    # Capture the desired key from the user. This should be the absolute path to the signed .key file
    targetSite["certKey"] = input(style.BOLD + "Certificate key (.key) [" + defaultCertKeyFile + "]: " + style.END).strip()
    if not targetSite["certKey"]: targetSite["certKey"] = defaultCertKeyFile

    # Default to the current certificate file, if there is one. Otherwise, assume siteName.crt
    defaultCertFile = targetSite["certificate"]
    if not defaultCertFile: defaultCertFile = targetSite["userHome"] + "/certificates/" + targetSite["siteName"] + ".crt"

    # Capture the desired certificate from the user. This should be the absolute path to the signed .crt file
    targetSite["certificate"] = input(style.BOLD + "Certificate (.crt) [" + defaultCertFile + "]: " + style.END).strip()
    if not targetSite["certificate"]: targetSite["certificate"] = defaultCertFile

    # Save the dictionary with the updated certificate and key file paths
    writeSiteConfig(targetSite)
    #print(currentSite["importFile"])

    return targetSite


def addCertificate(targetSite):
    # The config will always start with the default configuration
    # Any user customizations will be overwritten
    shutil.copyfile(quiverHome + "/base/default_https.conf", quiverHome + "/tmp/thttpsconf")

    print(style.BOLD + "Adding SSL certificate paths to the Apache configuration" + style.END)

    runCommand("sed -i \"s|__CORECONFIG__|" + targetSite["domainConfig"] + "|g\" " + quiverHome + "/tmp/thttpsconf")
    runCommand("sed -i \"s|__CERTKEYFILE__|" + targetSite["certKey"] + "|g\" " + quiverHome + "/tmp/thttpsconf")
    runCommand("sed -i \"s|__CERTFILE__|" + targetSite["certificate"] + "|g\" " + quiverHome + "/tmp/thttpsconf")

    runCommand("mv " + quiverHome + "/tmp/thttpsconf " + targetSite["apacheConfig"], True)
    runCommand("chown root: " + targetSite["apacheConfig"], True)

    # Enable the site
    runCommand("a2ensite " + targetSite["siteName"], True)

    # Enable the mod_ssl module
    runCommand("a2enmod ssl", True)



