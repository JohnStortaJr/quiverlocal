#!/usr/bin/python3

import os
import subprocess
import random
from smlib.format import *
#from smlib.info import *

# Quiver directories
quiverHome = os.getcwd()
quiverDB = quiverHome + "/sitedb/"

siteTemplate = {
    "siteName": "site99",
    "domainName": "site99.local",
    "serverAdmin": "user@localhost",
    "dbName": "site99_db",
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
    "certName": "",
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

siteTemplate["serverAdmin"] = siteTemplate["userName"] + "@" + siteTemplate["domainName"]
siteTemplate["domainRoot"] = siteTemplate["userHome"] + "/domains"
siteTemplate["domainHome"] = siteTemplate["domainRoot"] + "/" + siteTemplate["domainName"]
siteTemplate["domainConfig"] = siteTemplate["domainHome"] + "/domains/config/" + siteTemplate["domainName"] + ".core"
siteTemplate["apacheConfig"] = siteTemplate["apacheHome"] + "/sites-available/" + siteTemplate["domainName"] + ".conf"
siteTemplate["importPath"] = siteTemplate["userHome"] + "/exports"

# Cleans troublesome characters from a string
# There is a default list of characters, but a custom list can be provided
# You can specify if the custom list should be used instead of the defaults or appended to that list
# The default list includes most special characters with the exception of '.' and '@'
def cleanString(targetString, customChars=[" "], append=True):
    defaultChars = ["!", "#", "$", "%", "^", "&", "*", "(", ")", "=", "+", "{", "}", "[", "]", "|", "\\", ";", ":", "'", "\"", "/", "?", ",", "<", ">", "`", "~"]

    if append: badChars = defaultChars + customChars
    else: badChars = customChars

    for i in badChars:
        targetString = targetString.replace(i, '_')
    
    return targetString


# Prompt for input and return the value. Require an Int if desired.
def getInput(promptString, requireInt=False):
    enteredValue = input(promptString).strip()

    if requireInt and not enteredValue.isnumeric():
        print("")
        print(background.BCYAN + "Please enter a numeric value" + background.END)
        enteredValue = input(promptString).strip()

    return enteredValue


# Build a temporary bash script to run a linux command
# For use in cases where there is not a clean python-native way to perform a task
def runCommand(commandString="whoami", asRoot=False):
    localPID = random.randint(111111, 999999)
    tempScriptName = quiverHome + "/tmp/" + "tScript" + str(localPID)

    # Create script file and write commands to be executed
    with open(tempScriptName, "a") as outFile:
        outFile.write("#!/usr/bin/bash\n")
        outFile.write(commandString + "\n")

    # Make the script executable
    subprocess.run(["chmod", "755", tempScriptName], capture_output=True, text=True)

    # Run the script and display the output (end='' removes the blank line at the end)
    if asRoot:
        tempScriptResult = subprocess.run(["sudo", tempScriptName], capture_output=True, text=True)
    else:
        tempScriptResult = subprocess.run([tempScriptName], capture_output=True, text=True)

    # Delete the temporary script
    subprocess.run(["rm", tempScriptName], capture_output=True, text=True)

    # If stderr contains anything, print it immediately
    if tempScriptResult.stderr.strip(): print("e:" + tempScriptResult.stderr)

    # Return the stdout from the execution
    return tempScriptResult.stdout.strip()




def installDependencies():
    print(style.BOLD + "Installing Dependencies..." + style.END)
    runCommand("apt --yes install apache2 ghostscript libapache2-mod-php mysql-server php php-bcmath php-curl php-imagick php-intl php-json php-mbstring php-mysql php-xml php-zip", True)


def restartApache():
    runCommand("systemctl restart apache2", True)

