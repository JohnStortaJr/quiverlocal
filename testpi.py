#!/usr/bin/python3

import sys
import json
import os
import subprocess
import random

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

userHome = os.path.expanduser('~')

userName = runCommand("whoami", True)
print(userName.strip() + "---" + userHome)

userName = runCommand("whoami", False)
print(userName.strip() + "---" + userHome)

# Test a more complicated command
certHome = userHome + "/certificates"
certName = "myNewCert"
runCommand("curl https://wordpress.org/latest.tar.gz | tar zx -C " + userHome + "/domains")

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