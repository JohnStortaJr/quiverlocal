#!/usr/bin/python3

from smlib.core import *
from smlib.info import *
from smlib.format import *
import random
import json
import shutil
import secrets

def createNewSite():
    #os.system('clear')
    print("")
    print(color.BBLUE + "This will create a new local site using the information you provide " + color.END)

    getSiteName()
    getDomainName()
    getServerAdmin()
    getDatabaseName()
    getDatabaseUser()
    getDatabasePassword()

    if isSiteInfoCorrect():
        print("")
        print(style.BOLD + "Building site " + currentSite["siteName"] + style.END)
        # Build site
        installDependencies()
        installWordPress()
        changeApacheOwnership()
        configureApache()
        createDatabase()
        configureWordPressDatabaseConnection()
        getTablePrefix()
        restartApache()
        writeSiteConfig(currentSite)
        #print(json.dumps(currentSite, indent=4))

        print("")
        print(background.BCYAN + "Site " + currentSite["siteName"] + " has been created." + background.END)
        print("Make sure that your local " + style.BOLD + "C:\Windows\System32\drivers\etc\hosts" + style.END + " file contains these entries...")
        print(32 * "-")
        print("::1 " + currentSite["domainName"])
        print("127.0.0.1 " + currentSite["domainName"])
        print(32 * "-")
        print("Once the host entries are in place, \nyou can access the site using " + style.BOLD + "http://" + currentSite["domainName"] + style.END + " to complete the WordPress configuration.")
        print(style.ITALIC + "Be sure to complete the WordPress configuration BEFORE doing anything else with this site." + style.END)
    else:
        print("")
        print("Please make the desired changes and try again." + style.ITALIC + " (no changes made)" + style.END)

def importSite():
    print("")
    print(color.BBLUE + "This will create a new local site using the information you provide " + color.END)

    getSiteName()
    getDomainName()
    getServerAdmin()
    getDatabaseName()
    getDatabaseUser()
    getDatabasePassword()
    getImportFile()
    getImportData()

    if isSiteInfoCorrect(True):
        print("")
        print(style.BOLD + "Importing site " + currentSite["siteName"] + style.END)
        # Import site
        installDependencies()
        importFiles()
        changeApacheOwnership()
        configureApache()
        createDatabase()
        configureWordPressDatabaseConnection()
        getTablePrefix()
        importData()
        updateSiteValues(currentSite)
        restartApache()
        writeSiteConfig(currentSite)
        #print(json.dumps(currentSite, indent=4))

        print("")
        print(background.BCYAN + "Site " + currentSite["siteName"] + " has been imported." + background.END)
        print("Make sure that your local " + style.BOLD + "C:\Windows\System32\drivers\etc\hosts" + style.END + " file contains these entries...")
        print(32 * "-")
        print("::1 " + currentSite["domainName"])
        print("127.0.0.1 " + currentSite["domainName"])
        print(32 * "-")
        print("Once the host entries are in place, \nyou can access the site using " + style.BOLD + "http://" + currentSite["domainName"] + style.END)
    else:
        print("Please make the desired changes and try again." + style.ITALIC + " (no changes made)" + style.END)


### Download and extract the latest WordPress version
### Rename the folder to match the domain name and create a new wp-config file from the sample included in the download
def installWordPress():
    print(style.BOLD + "Installing WordPress..." + style.END)
    runCommand("curl https://wordpress.org/latest.tar.gz | tar zx -C " + currentSite["domainRoot"])
    os.rename(currentSite["domainRoot"] + "/wordpress", currentSite["domainHome"])
    shutil.copyfile(currentSite["domainHome"] + "/wp-config-sample.php", currentSite["domainHome"] + "/wp-config.php")


def importFiles():
    print(style.BOLD + "Importing WordPress files from " + style.END + currentSite["importFile"])

    os.mkdir(currentSite["domainHome"])
    runCommand("tar -xzvf " + currentSite["importFile"] + " -C " + currentSite["domainHome"] +  " --strip-components=1")



def getTablePrefix():
    # a test function just to try to extract the table_prefix from the wp-config.php file
    # The [1:-3] extracts a substring starting at the 2nd character until the 3 character from the end
    currentSite["tablePrefix"] = runCommand("awk '/table_prefix/{print $3}' " + currentSite["domainHome"] + "/wp-config.php")[1:-3]



def importData():
    print(style.BOLD + "Importing WordPress data from " + style.END + currentSite["importData"])

    runCommand("gzip -d " + currentSite["importData"])
    runCommand("mysql -u root " + currentSite["dbName"] + " < " + currentSite["importData"][:-3], True)
    runCommand("gzip " + currentSite["importData"][:-3])



def updateSiteValues(targetSite, protocol="http"):
    print(style.BOLD + "Updating local site URLs" + style.END)
    # Need to change the siteurl and home values
    commandString = "mysql -u root " + targetSite["dbName"] + " -e \"UPDATE " + targetSite["tablePrefix"] + "_options SET option_value = '" + protocol + "://" + targetSite["domainName"] + "' WHERE option_name = 'siteurl';\""
    #print(commandString)
    runCommand(commandString, True)

    commandString = "mysql -u root " + targetSite["dbName"] + " -e \"UPDATE " + targetSite["tablePrefix"] + "_options SET option_value = '" + protocol + "://" + targetSite["domainName"] + "' WHERE option_name = 'home';\""
    #print(commandString)
    runCommand(commandString, True)




### This will change the Apache global configuration so that it runs are the current user rather than www-data
### As a result of this, sites on this server must all be owned by the same user
def changeApacheOwnership():
    # Create backup and temp envvars files
    shutil.copyfile(currentSite["apacheHome"] + "/envvars", quiverHome + "/tmp/tenvvars.bak")
    shutil.copyfile(currentSite["apacheHome"] + "/envvars", quiverHome + "/tmp/tenvvars")
    
    # Change values so that Apache runs as current user
    runCommand("sed -i 's/APACHE_RUN_USER=www-data/APACHE_RUN_USER=" + currentSite["userName"] + "/g' " + quiverHome + "/tmp/tenvvars")
    runCommand("sed -i 's/APACHE_RUN_GROUP=www-data/APACHE_RUN_GROUP=" + currentSite["userName"] + "/g' " + quiverHome + "/tmp/tenvvars")
    
    # Overwrite envvars configuration (runAs ROOT)
    runCommand("mv " + quiverHome + "/tmp/tenvvars " + currentSite["apacheHome"] + "/envvars", True)
    runCommand("chown root: " + currentSite["apacheHome"] + "/envvars", True)


def configureApache():
    print(style.BOLD + "Configuring the Apache web server" + style.END)
    # This first step is to create the core domain configuration that will be used for all Virtual Hosts
    runCommand("sed 's|__SERVERADMIN__|" + currentSite["serverAdmin"] + "|g' " + quiverHome + "/base/default.core > " + quiverHome + "/tmp/tcoreconf")
    runCommand("sed -i 's|__DOMAINNAME__|" + currentSite["domainName"] + "|g' " + quiverHome + "/tmp/tcoreconf")
    runCommand("sed -i 's|__DOMAINDIR__|" + currentSite["domainHome"] + "|g' " + quiverHome + "/tmp/tcoreconf")
    shutil.copyfile(quiverHome + "/tmp/tcoreconf", currentSite["domainConfig"])

    # Next we need to create the Apache configuration files for this site
    shutil.copyfile(quiverHome + "/base/default_http.conf", quiverHome + "/tmp/thttpconf")

    runCommand("sed -i \"s|__CORECONFIG__|" + currentSite["domainConfig"] + "|g\" " + quiverHome + "/tmp/thttpconf")

    runCommand("mv " + quiverHome + "/tmp/thttpconf " + currentSite["apacheConfig"], True)
    runCommand("chown root: " + currentSite["apacheConfig"], True)

    # Enable the site
    runCommand("a2ensite " + currentSite["siteName"], True)

    # Disable the default site
    runCommand("a2ensite 000-default", True)

    # Enable the mod_rewrite module
    runCommand("a2enmod rewrite", True)


def createDatabase():
    shutil.copyfile(quiverHome + "/base/default_dbsetup.sql", quiverHome + "/tmp/tdbconf")
    runCommand("sed -i \"s|__DBNAME__|" + currentSite["dbName"] + "|g\" " + quiverHome + "/tmp/tdbconf")
    runCommand("sed -i \"s|__DBUSER__|" + currentSite["dbUser"] + "|g\" " + quiverHome + "/tmp/tdbconf")
    runCommand("sed -i \"s|__DBPASS__|" + currentSite["dbPass"] + "|g\" " + quiverHome + "/tmp/tdbconf")

    runCommand("mysql -u root < " + quiverHome + "/tmp/tdbconf", True)


def configureWordPressDatabaseConnection():
    print(style.BOLD + "Updating WordPress database connection information" + style.END)
    shutil.copyfile(currentSite["domainHome"] + "/wp-config.php", quiverHome + "/tmp/twpconf")

    # Remove cache entry
    runCommand("sed -i '/WPCACHEHOME/d' " + quiverHome + "/tmp/twpconf")

    # Replace database connection information with local values
    NEW_DB_NAME_STRING="define( 'DB_NAME', '" + currentSite["dbName"] + "' );"
    NEW_DB_USER_STRING="define( 'DB_USER', '" + currentSite["dbUser"] + "' );"
    NEW_DB_PASS_STRING="define( 'DB_PASSWORD', '" + currentSite["dbPass"] + "' );"
    NEW_DB_HOST_STRING="define( 'DB_HOST', 'localhost' );"
    runCommand("sed -i \"s|.*'DB_NAME'.*|" + NEW_DB_NAME_STRING + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'DB_USER'.*|" + NEW_DB_USER_STRING + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'DB_PASSWORD'.*|" + NEW_DB_PASS_STRING + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'DB_HOST'.*|" + NEW_DB_HOST_STRING + "|g\" " + quiverHome + "/tmp/twpconf")

    # Update SALT keys
    NEW_AUTH_KEY="define( 'AUTH_KEY',         '" + secrets.token_hex(32) + "' );"
    NEW_SECURE_AUTH_KEY="define( 'SECURE_AUTH_KEY',  '" + secrets.token_hex(32) + "' );"
    NEW_LOGGED_IN_KEY="define( 'LOGGED_IN_KEY',    '" + secrets.token_hex(32) + "' );"
    NEW_NONCE_KEY="define( 'NONCE_KEY',        '" + secrets.token_hex(32) + "' );"
    NEW_AUTH_SALT="define( 'AUTH_SALT',        '" + secrets.token_hex(32) + "' );"
    NEW_SECURE_AUTH_SALT="define( 'SECURE_AUTH_SALT', '" + secrets.token_hex(32) + "' );"
    NEW_LOGGED_IN_SALT="define( 'LOGGED_IN_SALT',   '" + secrets.token_hex(32) + "' );"
    NEW_NONCE_SALT="define( 'NONCE_SALT',       '" + secrets.token_hex(32) + "' );"

    runCommand("sed -i \"s|.*'AUTH_KEY'.*|" + NEW_AUTH_KEY + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'SECURE_AUTH_KEY'.*|" + NEW_SECURE_AUTH_KEY + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'LOGGED_IN_KEY'.*|" + NEW_LOGGED_IN_KEY + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'NONCE_KEY'.*|" + NEW_NONCE_KEY + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'AUTH_SALT'.*|" + NEW_AUTH_SALT + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'SECURE_AUTH_SALT'.*|" + NEW_SECURE_AUTH_SALT + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'LOGGED_IN_SALT'.*|" + NEW_LOGGED_IN_SALT + "|g\" " + quiverHome + "/tmp/twpconf")
    runCommand("sed -i \"s|.*'NONCE_SALT'.*|" + NEW_NONCE_SALT + "|g\" " + quiverHome + "/tmp/twpconf")

    shutil.copyfile(quiverHome + "/tmp/twpconf", currentSite["domainHome"] + "/wp-config.php")



# Get User Inputs
def getSiteName():
    defaultSiteName = "localdev" + str(random.randint(1111, 9999))
    currentSite["siteName"] = input(style.BOLD + "Site name [" + defaultSiteName + "]: " + style.END).strip()
    if not currentSite["siteName"]: currentSite["siteName"] = defaultSiteName

    currentSite["siteName"] = cleanString(currentSite["siteName"])

    # Set related values
    currentSite["domainConfig"] = currentSite["userHome"] + "/domains/config/" + currentSite["siteName"] + ".core"
    currentSite["apacheConfig"] = currentSite["apacheHome"] + "/sites-available/" + currentSite["siteName"] + ".conf"

    #print(currentSite["siteName"])


def getDomainName():
    defaultDomainName = currentSite["siteName"] + ".local"
    currentSite["domainName"] = input(style.BOLD + "Domain name [" + defaultDomainName + "]: " + style.END).strip()
    if not currentSite["domainName"]: currentSite["domainName"] = defaultDomainName

    # Set related values
    currentSite["domainHome"] = currentSite["userHome"] + "/domains/" + currentSite["domainName"]
    currentSite["serverAdmin"] = currentSite["userName"] + "@" + currentSite["domainName"]

    currentSite["domainName"] = cleanString(currentSite["domainName"])
    #print(currentSite["domainName"])


def getServerAdmin():
    defaultServerAdmin = currentSite["userName"] + "@" + currentSite["domainName"]
    currentSite["serverAdmin"] = input(style.BOLD + "Server admin [" + defaultServerAdmin + "]: " + style.END).strip()
    if not currentSite["serverAdmin"]: currentSite["serverAdmin"] = defaultServerAdmin

    #print(currentSite["serverAdmin"])


def getDatabaseName():
    defaultDatabaseName = cleanString(currentSite["siteName"], True) + "_db"
    currentSite["dbName"] = input(style.BOLD + "Database name [" + defaultDatabaseName + "]: " + style.END).strip()
    if not currentSite["dbName"]: currentSite["dbName"] = defaultDatabaseName

    currentSite["dbName"] = cleanString(currentSite["dbName"])
    #print(currentSite["dbName"])


def getDatabaseUser():
    defaultDatabaseUser = "wordpress"
    currentSite["dbUser"] = input(style.BOLD + "Database username [" + defaultDatabaseUser + "]: " + style.END).strip()
    if not currentSite["dbUser"]: currentSite["dbUser"] = defaultDatabaseUser

    currentSite["dbUser"] = cleanString(currentSite["dbUser"])
    #print(currentSite["dbUser"])


def getDatabasePassword():
    defaultDatabasePass = "start123"
    currentSite["dbPass"] = input(style.BOLD + "Database password [" + defaultDatabasePass + "]: " + style.END).strip()
    if not currentSite["dbPass"]: currentSite["dbPass"] = defaultDatabasePass

    currentSite["dbPass"] = cleanString(currentSite["dbPass"])
    #print(currentSite["dbPass"])


def getImportFile():
    defaultImportFile = currentSite["userHome"] + "/exports/" + currentSite["siteName"] + ".tar.gz"
    currentSite["importFile"] = input(style.BOLD + "Import File [" + defaultImportFile + "]: " + style.END).strip()
    if not currentSite["importFile"]: currentSite["importFile"] = defaultImportFile

    #print(currentSite["importFile"])


def getImportData():
    defaultImportData = currentSite["userHome"] + "/exports/" + currentSite["siteName"] + ".sql.gz"
    currentSite["importData"] = input(style.BOLD + "Import Data [" + defaultImportData + "]: " + style.END).strip()
    if not currentSite["importData"]: currentSite["importData"] = defaultImportData

    #print(currentSite["importData"])


def isSiteInfoCorrect(isImport=False):
    print("")
    print(style.UNDERLINE + "Confirm you wish to build a new local site with these details" + style.END)
    print(style.BOLD + "Site name: " + style.END + currentSite["siteName"])
    print(style.BOLD + "Domain name: " + style.END + currentSite["domainName"])
    print(style.BOLD + "Server admin: " + style.END + currentSite["serverAdmin"])
    print(style.BOLD + "Database Name: " + style.END + currentSite["dbName"])
    print(style.BOLD + "Database Username: " + style.END + currentSite["dbUser"])
    print(style.BOLD + "Database Password: " + style.END + currentSite["dbPass"])
    print("")
    print(style.ITALIC + "** Fixed Values **" + style.END)
    print(style.BOLD + "Domain Home: " + style.END + currentSite["domainHome"])
    print(style.BOLD + "Domain Config: " + style.END + currentSite["domainConfig"])
    print(style.BOLD + "Apache Home: " + style.END + currentSite["apacheHome"])
    print(style.BOLD + "Apache Config: " + style.END + currentSite["apacheConfig"])
    print(style.BOLD + "Apache Logs: " + style.END + currentSite["apacheLog"])

    if isImport:
        print(style.BOLD + "Import File: " + style.END + currentSite["importFile"])
        print(style.BOLD + "Import Data: " + style.END + currentSite["importData"])

    confirmation = input(style.BOLD + "Proceed [y/N]? " + style.END).strip()
    
    if confirmation == "y" or confirmation == "Y": return True
    
    return False

