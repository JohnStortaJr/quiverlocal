#!/usr/bin/python3

import os
import subprocess
import random
from smlib.format import *
#from smlib.info import *

# Quiver directories
quiverHome = os.getcwd()
quiverDB = quiverHome + "/sitedb/"

currentSite = {
    "siteName": "server99",
    "domainName": "server99.local",
    "serverAdmin": "user@localhost",
    "dbName": "localdev04_db",
    "tablePrefix": "wp_",
    "userName": os.environ.get("USER"),
    "userHome": os.environ.get("HOME"),
    "domainRoot": "",
    "domainHome": "",
    "domainConfig": "",
    "apacheHome": "/etc/apache2",
    "apacheConfig": "",
    "apacheLog": "/var/log/apache2",
    "isTrusted": False,
    "certPath": "",
    "certName": "MyCert",
    "certDuration": 365,
    "certKey": "",
    "certificate": "",
    "certRequest": "",
    "certConfig": "",
    "certRootKey": "",
    "certRoot": "",
    "dbUser": "wordpress",
    "dbPass": "start123",
    "importPath": "",
    "importFile": "NA",
    "importData": "NA"
}

currentSite["serverAdmin"] = currentSite["userName"] + "@" + currentSite["domainName"]
currentSite["domainRoot"] = currentSite["userHome"] + "/domains"
currentSite["domainHome"] = currentSite["domainRoot"] + "/" + currentSite["domainName"]
currentSite["domainConfig"] = currentSite["domainHome"] + "/domains/config/" + currentSite["domainName"] + ".core"
currentSite["apacheConfig"] = currentSite["apacheHome"] + "/sites-available/" + currentSite["domainName"] + ".conf"
currentSite["importPath"] = currentSite["userHome"] + "/exports"

def cleanString(dirtyString, cleanPeriods=False):
    badChars = [';', ':', '!', "*", "\\", "/", ",", " "]

    if cleanPeriods: badChars.append(".")

    for i in badChars:
        dirtyString = dirtyString.replace(i, '_')
    
    return dirtyString

def getInput(promptString, requireInt=False):
    enteredValue = input(promptString).strip()

    if requireInt and not enteredValue.isnumeric():
        print("")
        print(background.BCYAN + "Please enter a numeric value" + background.END)
        enteredValue = input(promptString).strip()

    return enteredValue


def runCommand(commandString="whoami", asRoot=False):
    localPID = random.randint(111111, 999999)
    tempScriptName = quiverHome + "/tmp/" + "tScript" + str(localPID)
    #print(tempScriptName + "-" + commandString)

    # Create script file and write commands to be executed
    with open(tempScriptName, "a") as outFile:
        outFile.write("#!/usr/bin/bash\n")
        outFile.write(commandString + "\n")

    # Make the script executable
    subprocess.run(["chmod", "755", tempScriptName], capture_output=True, text=True)

    # Run the script and display the output (end='' removes the blank line at the end)
    if asRoot:
        #print("Running as ROOT")
        tempScriptResult = subprocess.run(["sudo", tempScriptName], capture_output=True, text=True)
    else:
        #print("Running as User")
        tempScriptResult = subprocess.run([tempScriptName], capture_output=True, text=True)

    # Delete the temporary script
    
    subprocess.run(["rm", tempScriptName], capture_output=True, text=True)
    if tempScriptResult.stderr.strip(): print("e:" + tempScriptResult.stderr)

    return tempScriptResult.stdout.strip()




def installDependencies():
    print(style.BOLD + "Installing Dependencies..." + style.END)
    runCommand("apt --yes install apache2 ghostscript libapache2-mod-php mysql-server php php-bcmath php-curl php-imagick php-intl php-json php-mbstring php-mysql php-xml php-zip", True)


def restartApache():
    runCommand("systemctl restart apache2", True)

