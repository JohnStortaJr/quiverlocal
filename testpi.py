#!/usr/bin/python3

import sys
import json
import os
import subprocess
import random
from smlib.format import *

quiverHome = os.getcwd()
userHome = "/home/jstorta"

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
        print("Running as ROOT")
        tempScriptResult = subprocess.run(["sudo", tempScriptName], capture_output=True, text=True)
    else:
        print("Running as User")
        tempScriptResult = subprocess.run([tempScriptName], capture_output=True, text=True)

    # Delete the temporary script
    
    subprocess.run(["rm", tempScriptName], capture_output=True, text=True)
    return tempScriptResult.stdout

def readSiteConfig(siteName):
    # Open JSON file named site.Name.json in the configdb directory
    # Read the contents into a dictionary
    with open(quiverHome + "/sitedb/" + siteName + ".json", 'r') as inFile:
        activeSite = json.load(inFile)

    # Print the dictionary
    print(json.dumps(activeSite, indent=4, sort_keys=True))
    #print(activeSite)
    return activeSite

def writeSiteConfig(siteName, siteDictionary):
    # Open JSON file named siteName.json in the configdb directory
    # Write the contents of the activeSite dictionary to the file
    with open(quiverHome + "/sitedb/" + siteName + ".json", 'w') as outFile:
        json.dump(siteDictionary, outFile, indent=4)
        outFile.write("\n")


testSite = {
    "site": {
        "name": "localdev04"
    },
    "user": {
        "name": os.environ.get("USER"),
        "home": os.environ.get("HOME")
    },
    "domain": {
        "name": "localdev04.local",
        "home": "",
        "config": ""
    },
    "database": {
        "name": "localdev04_db",
        "user": "wordpress",
        "password": "start123"
    },
    "apache": {
        "root": "/etc/apache2",
        "log": "/var/log/apache2",
        "config": ""
    },
    "import": {
        "path": "",
        "file": "",
        "data": ""
    },
    "certificate": {
        "path": "",
        "name": "MyCert",
        "duration": 365,
        "key_file": "",
        "cert_file": "",
        "cert_request": "",
        "cert_config": "",
        "root_key_file": "",
        "root_cert_file": ""
    }
}

testSite["domain"]["home"] = testSite["user"]["home"] + "/domains/" + testSite["domain"]["name"]
testSite["domain"]["config"] = testSite["domain"]["home"] + "/domains/config/" + testSite["domain"]["name"] + ".core"
testSite["apache"]["config"] = testSite["apache"]["root"] + "/sites-available/" + testSite["domain"]["name"] + ".conf"
testSite["import"]["path"] = testSite["user"]["home"] + "/exports"
testSite["import"]["file"] = testSite["user"]["home"] + "/exports/NOFILE"
testSite["import"]["data"] = testSite["user"]["home"] + "/exports/NODATA"
testSite["certificate"]["path"] = testSite["user"]["home"] + "/certificates"
testSite["certificate"]["key_file"] = testSite["user"]["home"] + "/certificates/myCert.key"
testSite["certificate"]["cert_file"] = testSite["user"]["home"] + "/certificates/myCert.crt"
testSite["certificate"]["cert_request"] = testSite["user"]["home"] + "/certificates/myCert.csr"
testSite["certificate"]["cert_config"] = testSite["user"]["home"] + "/certificates/myCert.ext"
testSite["certificate"]["root_key_file"] = testSite["user"]["home"] + "/certificates/myCA.key"
testSite["certificate"]["root_cert_file"] = testSite["user"]["home"] + "/certificates/myCA.pem"


print(json.dumps(testSite, indent=4))




#print("Run sudo command with list of words")
#subprocess.run(["sudo", "-k"])
#result1 = subprocess.run(["sudo", "ls", "/root"], capture_output=True, text=True)
#print(result1.stdout, end='')

#print("")
#print("Run sudo command by creating temp file and executing the file")
# Create temporary script
#tempscript="tmpfile"
#outfile = open(tempscript, "w")
#outfile.write("ls /root")
#utfile.close()

# Make the script executable
#subprocess.run(["chmod", "755", quiver_home + "/" + tempscript], capture_output=True, text=True)

# Run the script and display the output (end='' removes the blank line at the end)
#result2 = subprocess.run(["sudo", quiver_home + "/" + tempscript], capture_output=True, text=True)
#print(result2.stdout, end='')

# Delete the temporary script
#subprocess.run(["rm", quiver_home + "/" + tempscript], capture_output=True, text=True)

#userHome = os.path.expanduser('~')

#userName = runCommand("whoami", True)
#print(userName.strip() + "---" + userHome)

#userName = runCommand("whoami", False)#
#print(userName.strip() + "---" + userHome)

# Test a more complicated command
#certHome = userHome + "/certificates"
#certName = "myNewCert"
#runCommand("curl https://wordpress.org/latest.tar.gz | tar zx -C " + userHome + "/domains")

#siteName = "newdomain01"
#print("\nConfiguration Details for : " + siteName)
#activeSite = readSiteConfig(siteName)

#print("Database: " + activeSite["db_name"])
#print("Domain Name: " + activeSite["domain_name"])


#siteName = "newdomain01"
#activeSite["site_name"] = siteName
#activeSite["domain_name"] = siteName + ".local"
#print(json.dumps(activeSite, indent=4, sort_keys=True))

#writeSiteConfig(siteName, activeSite)

currentSite = {
  "siteName": "dev2.johnstortajr",
  "domainName": "dev2.johnstortajr.local",
  "dbName": "dev2_johnstortajr_db",
  "tablePrefix": "wp_eduxzu",
  "userName": "jstorta",
  "userHome": "/home/jstorta",
  "domainHome": "/home/jstorta/domains/dev2.johnstortajr.local",
  "domainConfig": "/home/jstorta/domains/config/dev2.johnstortajr.core",
  "apacheHome": "/etc/apache2",
  "apacheConfig": "/etc/apache2/sites-available/dev1.johnstortajr.conf",
  "apacheLog": "/var/log/apache2",
  "isTrusted": False,
  "certPath": "/home/jstorta/certificates",
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
  "importPath": "/home/jstorta/exports",
  "importFile": "/home/jstorta/exports/johnstortajr.tar.gz",
  "importData": "/home/jstorta/exports/storozon_com.sql.gz"
}

#commandString = "mysql -u root " + currentSite["dbName"] + " -e \"UPDATE " + currentSite["tablePrefix"] + "_options SET option_value = 'http://" + currentSite["domainName"] + "' WHERE option_name = 'site_url';\""

#print(commandString)
#runCommand(commandString, True)

print(color.BLACK + "This is a color test string " + color.END + " >> BLACK")
print(color.RED + "This is a color test string " + color.END + " >> RED")
print(color.GREEN + "This is a color test string " + color.END + " >> GREEN")
print(color.YELLOW + "This is a color test string " + color.END + " >> YELLOW")
print(color.BLUE + "This is a color test string " + color.END + " >> BLUE")
print(color.MAGENTA + "This is a color test string " + color.END + " >> MAGENTA")
print(color.CYAN + "This is a color test string " + color.END + " >> CYAN")
print(color.WHITE + "This is a color test string " + color.END + " >> WHITE")
print("")
print(color.BBLACK + "This is a color test string " + color.END + " >> BBLACK")
print(color.BRED + "This is a color test string " + color.END + " >> BRED")
print(color.BGREEN + "This is a color test string " + color.END + " >> BGREEN")
print(color.BYELLOW + "This is a color test string " + color.END + " >> BYELLOW")
print(color.BBLUE + "This is a color test string " + color.END + " >> BBLUE")
print(color.BMAGENTA + "This is a color test string " + color.END + " >> BMAGENTA")
print(color.BCYAN + "This is a color test string " + color.END + " >> BCYAN")
print(color.BWHITE + "This is a color test string " + color.END + " >> BWHITE")

print("")
print(background.BLACK + "This is a background color test string " + background.END + " >> BLACK")
print(background.RED + "This is a background color test string " + background.END + " >> RED")
print(background.GREEN + "This is a background color test string " + background.END + " >> GREEN")
print(background.YELLOW + "This is a background color test string " + background.END + " >> YELLOW")
print(background.BLUE + "This is a background color test string " + background.END + " >> BLUE")
print(background.MAGENTA + "This is a background color test string " + background.END + " >> MAGENTA")
print(background.CYAN + "This is a background color test string " + background.END + " >> CYAN")
print(background.WHITE + "This is a background color test string " + background.END + " >> WHITE")
print("")
print(background.BBLACK + "This is a background color test string " + background.END + " >> BBLACK")
print(background.BRED + "This is a background color test string " + background.END + " >> BRED")
print(background.BGREEN + "This is a background color test string " + background.END + " >> BGREEN")
print(background.BYELLOW + "This is a background color test string " + background.END + " >> BYELLOW")
print(background.BBLUE + "This is a background color test string " + background.END + " >> BBLUE")
print(background.BMAGENTA + "This is a background color test string " + background.END + " >> BMAGENTA")
print(background.BCYAN + "This is a background color test string " + background.END + " >> BCYAN")
print(background.BWHITE + "This is a background color test string " + background.END + " >> BWHITE")

print("")
print(style.BOLD + "This is a style test string " + style.END + " >> BOLD")
print(style.FAINT + "This is a style test string " + style.END + " >> FAINT")
print(style.ITALIC + "This is a style test string " + style.END + " >> ITALIC")
print(style.UNDERLINE + "This is a style test string " + style.END + " >> UNDERLINE")
print(style.BLINK + "This is a style test string " + style.END + " >> BLINK")
print(style.NEGATIVE + "This is a style test string " + style.END + " >> NEGATIVE")
print(style.CROSSED + "This is a style test string " + style.END + " >> CROSSED")
