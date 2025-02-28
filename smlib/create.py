#!/usr/bin/python3

from smlib.core import *
from smlib.format import *
from smlib.info import *
from smlib.collect import *
import shutil
import secrets


### Creates a new site using the latest WordPress distribution
def createNewSite():
    #os.system('clear')
    print("")
    print(color.BBLUE + "This will create a new local site using the information you provide " + color.END)

    newSite = siteTemplate.copy()

    newSite = getSiteName(newSite)
    newSite = getDomainName(newSite)
    newSite = getServerAdmin(newSite)
    newSite = getDatabaseName(newSite)
    newSite = getDatabaseUser(newSite)
    newSite = getDatabasePassword(newSite)

    if isSiteInfoCorrect(newSite):
        print("")
        print(style.BOLD + "Building site " + newSite["siteName"] + style.END)

        # Build site
        #installDependencies()
        #changeApacheOwnership(newSite)
        directoryCheck(newSite)
        installWordPress(newSite)
        configureApache(newSite)
        createDatabase(newSite)
        configureWordPressDatabaseConnection(newSite)
        newSite = getTablePrefix(newSite)
        restartApache()

        writeSiteConfig(newSite)

        print("")
        print(background.BCYAN + "Site " + newSite["siteName"] + " has been created." + background.END)
        print("Make sure that your local " + style.BOLD + "C:\Windows\System32\drivers\etc\hosts" + style.END + " file contains these entries...")
        print(32 * "-")
        print("::1 " + newSite["domainName"])
        print("127.0.0.1 " + newSite["domainName"])
        print(32 * "-")
        print("Once the host entries are in place, \nyou can access the site using " + style.BOLD + "http://" + newSite["domainName"] + style.END + " to complete the WordPress configuration.")
        print(style.ITALIC + "Be sure to complete the WordPress configuration BEFORE doing anything else with this site." + style.END)
    else:
        print("")
        print("Please make the desired changes and try again." + style.ITALIC + " (no changes made)" + style.END)


### Creates a new site using files and data exported from an existing WordPress site
def importSite():
    print("")
    print(color.BBLUE + "This will create a new local site using the information you provide " + color.END)

    newSite = siteTemplate.copy()

    newSite = getSiteName(newSite)
    newSite = getDomainName(newSite)
    newSite = getServerAdmin(newSite)
    newSite = getDatabaseName(newSite)
    newSite = getDatabaseUser(newSite)
    newSite = getDatabasePassword(newSite)
    newSite = getImportFile(newSite)
    newSite = getImportData(newSite)

    if isSiteInfoCorrect(newSite, True):
        print("")
        print(style.BOLD + "Importing site " + newSite["siteName"] + style.END)

        # Import site
        #installDependencies()
        #changeApacheOwnership(newSite)
        directoryCheck(newSite)
        importFiles(newSite)
        configureApache(newSite)
        createDatabase(newSite)
        configureWordPressDatabaseConnection(newSite)
        newSite = getTablePrefix(newSite)
        importData(newSite)
        updateSiteValues(newSite)
        restartApache()

        writeSiteConfig(newSite)

        print("")
        print(background.BCYAN + "Site " + newSite["siteName"] + " has been imported." + background.END)
        print("Make sure that your local " + style.BOLD + "C:\Windows\System32\drivers\etc\hosts" + style.END + " file contains these entries...")
        print(32 * "-")
        print("::1 " + newSite["domainName"])
        print("127.0.0.1 " + newSite["domainName"])
        print(32 * "-")
        print("Once the host entries are in place, \nyou can access the site using " + style.BOLD + "http://" + newSite["domainName"] + style.END)
    else:
        print("Please make the desired changes and try again." + style.ITALIC + " (no changes made)" + style.END)


### Provide the collected site details and ask for confirmation before proceeding
def isSiteInfoCorrect(targetSite, isImport=False):
    print("")
    print(style.UNDERLINE + "Confirm you wish to create a new local site with these details" + style.END)
    print(style.BOLD + "Site name: " + style.END + targetSite["siteName"])
    print(style.BOLD + "Domain name: " + style.END + targetSite["domainName"])
    print(style.BOLD + "Server admin: " + style.END + targetSite["serverAdmin"])
    print(style.BOLD + "Database Name: " + style.END + targetSite["dbName"])
    print(style.BOLD + "Database Username: " + style.END + targetSite["dbUser"])
    print(style.BOLD + "Database Password: " + style.END + targetSite["dbPass"])
    print("")
    print(style.ITALIC + "** Fixed Values **" + style.END)
    print(style.BOLD + "Domain Home: " + style.END + targetSite["domainHome"])
    print(style.BOLD + "Domain Config: " + style.END + targetSite["domainConfig"])
    print(style.BOLD + "Apache Home: " + style.END + targetSite["apacheHome"])
    print(style.BOLD + "Apache Config: " + style.END + targetSite["apacheConfig"])
    print(style.BOLD + "Apache Logs: " + style.END + targetSite["apacheLog"])

    if isImport:
        print(style.BOLD + "Import File: " + style.END + targetSite["importFile"])
        print(style.BOLD + "Import Data: " + style.END + targetSite["importData"])

    confirmation = input(style.BOLD + "Proceed [y/N]? " + style.END).strip()
    
    if confirmation == "y" or confirmation == "Y": return True
    
    return False


### This will change the Apache global configuration so that it runs are the current user rather than www-data
### As a result of this, sites on this server must all be owned by the same user
def changeApacheOwnership(targetSite):
    # Create backup and temp envvars files
    shutil.copyfile(targetSite["apacheHome"] + "/envvars", quiverHome + "/tmp/tenvvars")
    
    # Change values so that Apache runs as current user
    replaceFileText(quiverHome + "/tmp/tenvvars", "APACHE_RUN_USER=www-data", "APACHE_RUN_USER=" + targetSite["userName"])
    replaceFileText(quiverHome + "/tmp/tenvvars", "APACHE_RUN_GROUP=www-data", "APACHE_RUN_GROUP=" + targetSite["userName"])
    
    # Overwrite envvars configuration (runAs ROOT)
    runCommand("mv " + quiverHome + "/tmp/tenvvars " + targetSite["apacheHome"] + "/envvars", True)
    runCommand("chown root: " + targetSite["apacheHome"] + "/envvars", True)


### Rename the folder to match the domain name and create a new wp-config file from the sample included in the download
def installWordPress(targetSite):
    print(style.BOLD + "►►► Installing WordPress..." + style.END)

    runCommand("curl --output-dir " + quiverDB + "/imports" + " --create-dirs -O https://wordpress.org/latest.tar.gz")
    runCommand("mkdir -p " + targetSite["domainHome"])
    runCommand("tar -zxvf " + quiverDB + "/imports" + "/latest.tar.gz" + " -C " + targetSite["domainHome"] + " --strip-components=1")

    # Create the initial WordPress configuration file using the sample provided in the download
    shutil.copyfile(targetSite["domainHome"] + "/wp-config-sample.php", targetSite["domainHome"] + "/wp-config.php")


### Creates the configuration files needed for Apache
def configureApache(targetSite):
    print(style.BOLD + "►►► Configuring the Apache web server..." + style.END)

    # This first step is to create the core domain configuration that will be used for all Virtual Hosts
    # This file indicates the servername that ties this configuration to the request
    shutil.copyfile(quiverHome + "/base/default.core", quiverHome + "/tmp/tcoreconf")
    replaceFileText(quiverHome + "/tmp/tcoreconf", "__SERVERADMIN__", targetSite["serverAdmin"])
    replaceFileText(quiverHome + "/tmp/tcoreconf", "__DOMAINNAME__", targetSite["domainName"])
    replaceFileText(quiverHome + "/tmp/tcoreconf", "__DOMAINDIR__", targetSite["domainHome"])

    shutil.copyfile(quiverHome + "/tmp/tcoreconf", targetSite["domainConfig"])

    # Next we need to create the Apache configuration files for this site
    shutil.copyfile(quiverHome + "/base/default_http.conf", quiverHome + "/tmp/thttpconf")
    replaceFileText(quiverHome + "/tmp/thttpconf", "__CORECONFIG__", targetSite["domainConfig"])
    runCommand("mv " + quiverHome + "/tmp/thttpconf " + targetSite["apacheConfig"], True)
    runCommand("chown root: " + targetSite["apacheConfig"], True)

    # Enable the site
    runCommand("a2ensite " + targetSite["siteName"], True)

    # Disable the default site
    runCommand("a2dissite 000-default", True)

    # Enable the mod_rewrite module
    runCommand("a2enmod rewrite", True)


### This creates an empty database for the site
def createDatabase(targetSite):
    print(style.BOLD + "►►► Creating WordPress database..." + style.END)

    shutil.copyfile(quiverHome + "/base/default_dbsetup.sql", quiverHome + "/tmp/tdbconf")
    replaceFileText(quiverHome + "/tmp/tdbconf", "__DBNAME__", targetSite["dbName"])
    replaceFileText(quiverHome + "/tmp/tdbconf", "__DBUSER__", targetSite["dbUser"])
    replaceFileText(quiverHome + "/tmp/tdbconf", "__DBPASS__", targetSite["dbPass"])

    oldRunCommand("mysql -u root < " + quiverHome + "/tmp/tdbconf", True)


### This updates the wp-config file to point to the new database with all the correct login information
def configureWordPressDatabaseConnection(targetSite):
    print(style.BOLD + "►►► Updating WordPress database connection information..." + style.END)

    shutil.copyfile(targetSite["domainHome"] + "/wp-config.php", quiverHome + "/tmp/twpconf")

    # Remove cache entry (this is common on imported sites and will likely reference a production URL, which is not desired)
    replaceFileText(quiverHome + "/tmp/twpconf", "WPCACHEHOME", "")

    # Replace database connection information with local values
    NEW_DB_NAME_STRING="define( 'DB_NAME', '" + targetSite["dbName"] + "' );"
    NEW_DB_USER_STRING="define( 'DB_USER', '" + targetSite["dbUser"] + "' );"
    NEW_DB_PASS_STRING="define( 'DB_PASSWORD', '" + targetSite["dbPass"] + "' );"
    NEW_DB_HOST_STRING="define( 'DB_HOST', 'localhost' );"
    replaceFileText(quiverHome + "/tmp/twpconf", "DB_NAME", NEW_DB_NAME_STRING, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "DB_USER", NEW_DB_USER_STRING, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "DB_PASSWORD", NEW_DB_PASS_STRING, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "DB_HOST", NEW_DB_HOST_STRING, True)

    # Update SALT keys
    # These keys are different from the ones that the WordPress site creates.
    # The WP site includes all types of characters. But special characters cause problems for the script
    # so these keys use only alphanumeric characters
    NEW_AUTH_KEY="define( 'AUTH_KEY',         '" + secrets.token_hex(32) + "' );"
    NEW_SECURE_AUTH_KEY="define( 'SECURE_AUTH_KEY',  '" + secrets.token_hex(32) + "' );"
    NEW_LOGGED_IN_KEY="define( 'LOGGED_IN_KEY',    '" + secrets.token_hex(32) + "' );"
    NEW_NONCE_KEY="define( 'NONCE_KEY',        '" + secrets.token_hex(32) + "' );"
    NEW_AUTH_SALT="define( 'AUTH_SALT',        '" + secrets.token_hex(32) + "' );"
    NEW_SECURE_AUTH_SALT="define( 'SECURE_AUTH_SALT', '" + secrets.token_hex(32) + "' );"
    NEW_LOGGED_IN_SALT="define( 'LOGGED_IN_SALT',   '" + secrets.token_hex(32) + "' );"
    NEW_NONCE_SALT="define( 'NONCE_SALT',       '" + secrets.token_hex(32) + "' );"

    replaceFileText(quiverHome + "/tmp/twpconf", "'AUTH_KEY", NEW_AUTH_KEY, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "'SECURE_AUTH_KEY", NEW_SECURE_AUTH_KEY, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "'LOGGED_IN_KEY", NEW_LOGGED_IN_KEY, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "'NONCE_KEY", NEW_NONCE_KEY, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "'AUTH_SALT", NEW_AUTH_SALT, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "'SECURE_AUTH_SALT", NEW_SECURE_AUTH_SALT, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "'LOGGED_IN_SALT", NEW_LOGGED_IN_SALT, True)
    replaceFileText(quiverHome + "/tmp/twpconf", "'NONCE_SALT", NEW_NONCE_SALT, True)

    shutil.copyfile(quiverHome + "/tmp/twpconf", targetSite["domainHome"] + "/wp-config.php")


### The table prefix is needed to properly run SQL commands
### It is contained within the wp-config file and needs to be extracted
def getTablePrefix(targetSite):
    with open(targetSite["domainHome"] + "/wp-config.php", 'r') as inFile:
        # Read all lines form the file into a list
        configLines = inFile.readlines()

        # Check each line until finding table_prefix and then return that value
        for i in configLines:
            if "table_prefix" in i:
                foundLine = i
                break
        
        targetSite["tablePrefix"] =  foundLine.split("=")[1][2:-4]

    return targetSite


### Make sure all directories in the site paths exist (create as needed)
def directoryCheck(targetSite):
    if not os.path.exists(targetSite["domainRoot"]): 
        print("Creating path " + style.BOLD + targetSite["domainRoot"] + style.END)
        os.mkdir(targetSite["domainRoot"])

    if not os.path.exists(targetSite["domainRoot"] + "/config"): 
        print("Creating path " + style.BOLD + targetSite["domainRoot"] + "/config" + style.END)
        os.mkdir(targetSite["domainRoot"] + "/config")


### Import WordPress files from a user-specified export (tar.gz format)
def importFiles(targetSite):
    print(style.BOLD + "►►► Importing WordPress files from " + style.END + targetSite["importFile"] + "...")

    os.mkdir(targetSite["domainHome"])
    runCommand("tar -xzvf " + targetSite["importFile"] + " -C " + targetSite["domainHome"] +  " --strip-components=1")


### Import WordPress data from a user-specified export (sql.gz format)
def importData(targetSite):
    print(style.BOLD + "►►► Importing WordPress data from " + style.END + targetSite["importData"] + "...")

    runCommand("gzip -d " + targetSite["importData"])
    oldRunCommand("mysql -u root " + targetSite["dbName"] + " < " + targetSite["importData"][:-3], True)
    runCommand("gzip " + targetSite["importData"][:-3])


### Update the siteurl and home values in the WordPress database to match the local domain rather than the imported source
### Specify whether the target URL should use http or https
def updateSiteValues(targetSite, protocol="http"):
    print(style.BOLD + "►►► Updating local site URLs..." + style.END)
    # Need to change the siteurl and home values
    commandString = "mysql -u root " + targetSite["dbName"] + " -e \"UPDATE " + targetSite["tablePrefix"] + "_options SET option_value = '" + protocol + "://" + targetSite["domainName"] + "' WHERE option_name = 'siteurl';\""
    #print(commandString)
    oldRunCommand(commandString, True)

    commandString = "mysql -u root " + targetSite["dbName"] + " -e \"UPDATE " + targetSite["tablePrefix"] + "_options SET option_value = '" + protocol + "://" + targetSite["domainName"] + "' WHERE option_name = 'home';\""
    #print(commandString)
    oldRunCommand(commandString, True)



