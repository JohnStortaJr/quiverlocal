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
    "certDuration": 1825,
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
siteTemplate["certPath"] = siteTemplate["userHome"] + "/certificates/"

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
def oldRunCommand(commandString="whoami", asRoot=False):
    print(commandString)
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
    #subprocess.run(["rm", tempScriptName], capture_output=True, text=True)

    # If stderr contains anything, print it immediately
    if tempScriptResult.stderr.strip(): print("e:" + tempScriptResult.stderr)

    # Need to see if I can add a line to the script to capture and return the exit code. And then use that here to determine success/failure

    # Return the stdout from the execution
    return tempScriptResult.stdout.strip()


def runCommand(commandString="whoami", asRoot=False):
    commandList = commandString.split()
    print(commandString)

    # Clear cached sudo access (this is for testing purposes only)
    #subprocess.run(["sudo", "-k"], capture_output=True, text=True)

    # Add sudo as the first element if the command is to be run as root
    if asRoot:
        commandList.insert(0, "sudo")
    #print(commandList)

    tempScriptResult = subprocess.run(commandList, capture_output=True, text=True)
    print("e--->" + tempScriptResult.stderr)
    #print("##################################")
    #print("o--->" + tempScriptResult.stdout)
    
    # If stderr contains anything, print it immediately
    #if tempScriptResult.stderr.strip(): print("e:" + tempScriptResult.stderr)

    # Return the stdout from the execution
    return tempScriptResult.stdout.strip()


### Finds a pattern in a line of a given file and replaces the text. It can replace the entire line or just the targetText
def replaceFileText(targetFile, targetText, newText, wholeLine=False):
    with open(targetFile, 'r') as inFile:
        # Read all lines form the file into a list
        configLines = inFile.readlines()

        # Check each line until finding the value that needs to be replaced
        lineCounter = 0
        while lineCounter < len(configLines):
            if targetText in configLines[lineCounter]:
                if wholeLine:
                    # Replace the entire line
                    configLines[lineCounter] = newText + "\n"
                else:
                    # Only swap the targetText
                    configLines[lineCounter] = configLines[lineCounter].replace(targetText, newText)
            
            lineCounter += 1

    # Write out the config file with the updated line(s)
    with open(targetFile, 'w') as outFile:
        outFile.writelines(configLines)




def installDependencies():
    print(style.BOLD + "Installing Dependencies..." + style.END)
    runCommand("apt --yes install apache2 ghostscript libapache2-mod-php mysql-server php php-bcmath php-curl php-imagick php-intl php-json php-mbstring php-mysql php-xml php-zip", True)


def restartApache():
    runCommand("systemctl restart apache2", True)

