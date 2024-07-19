#!/usr/bin/python3

from smlib.core import *
from smlib.info import *
from smlib.format import *
import random

# Get User Inputs
def getSiteName(targetSite):
    defaultSiteName = "localdev" + str(random.randint(1111, 9999))
    uniqueSiteName = False

    while not uniqueSiteName:
        targetSite["siteName"] = input(style.BOLD + "Site name [" + defaultSiteName + "]: " + style.END).strip()
        if not targetSite["siteName"]: targetSite["siteName"] = defaultSiteName

        # Check to see if any existing sites use this same name
        uniqueSiteName = isUnique("siteName", targetSite["siteName"])

        if not uniqueSiteName: print(background.BYELLOW + "Site '" + targetSite["siteName"] + "' already exists!" + background.END)

    targetSite["siteName"] = cleanString(targetSite["siteName"])

    # Set related values
    targetSite["domainConfig"] = targetSite["userHome"] + "/domains/config/" + targetSite["siteName"] + ".core"
    targetSite["apacheConfig"] = targetSite["apacheHome"] + "/sites-available/" + targetSite["siteName"] + ".conf"

    return targetSite


def getDomainName(targetSite):
    defaultDomainName = targetSite["siteName"] + ".local"
    uniqueDomainName = False

    while not uniqueDomainName:
        targetSite["domainName"] = input(style.BOLD + "Domain name [" + defaultDomainName + "]: " + style.END).strip()
        if not targetSite["domainName"]: targetSite["domainName"] = defaultDomainName
        targetSite["domainName"] = cleanString(targetSite["domainName"])

        # Check to see if any existing sites use this same name
        uniqueDomainName = isUnique("domainName", targetSite["domainName"])

        if not uniqueDomainName: print(background.BYELLOW + "Domain '" + targetSite["domainName"] + "' already exists!" + background.END)

    # Set related values
    targetSite["domainHome"] = targetSite["userHome"] + "/domains/" + targetSite["domainName"]
    targetSite["serverAdmin"] = targetSite["userName"] + "@" + targetSite["domainName"]

    return targetSite


def getServerAdmin(targetSite):
    defaultServerAdmin = targetSite["userName"] + "@" + targetSite["domainName"]
    targetSite["serverAdmin"] = input(style.BOLD + "Server admin [" + defaultServerAdmin + "]: " + style.END).strip()
    if not targetSite["serverAdmin"]: targetSite["serverAdmin"] = defaultServerAdmin

    return targetSite


def getDatabaseName(targetSite):
    defaultDatabaseName = cleanString(targetSite["siteName"], ["."], True) + "_db"

    targetSite["dbName"] = cleanString(targetSite["dbName"])

    uniqueDatabaseName = False

    while not uniqueDatabaseName:
        targetSite["dbName"] = input(style.BOLD + "Database name [" + defaultDatabaseName + "]: " + style.END).strip()
        if not targetSite["dbName"]: targetSite["dbName"] = defaultDatabaseName
        targetSite["dbName"] = cleanString(targetSite["dbName"])

        # Check to see if any existing sites use this same name
        uniqueDatabaseName = isUnique("dbName", targetSite["dbName"])

        if not uniqueDatabaseName: print(background.BYELLOW + "Database '" + targetSite["dbName"] + "' already exists!" + background.END)

    return targetSite


def getDatabaseUser(targetSite):
    defaultDatabaseUser = "wordpress"
    targetSite["dbUser"] = input(style.BOLD + "Database username [" + defaultDatabaseUser + "]: " + style.END).strip()
    if not targetSite["dbUser"]: targetSite["dbUser"] = defaultDatabaseUser

    targetSite["dbUser"] = cleanString(targetSite["dbUser"])

    return targetSite


def getDatabasePassword(targetSite):
    defaultDatabasePass = "start123"
    targetSite["dbPass"] = input(style.BOLD + "Database password [" + defaultDatabasePass + "]: " + style.END).strip()
    if not targetSite["dbPass"]: targetSite["dbPass"] = defaultDatabasePass

    targetSite["dbPass"] = cleanString(targetSite["dbPass"])

    return targetSite


def getImportFile(targetSite):
    defaultImportFile = quiverDB + "/imports/" + targetSite["siteName"] + ".tar.gz"
    targetSite["importFile"] = input(style.BOLD + "Import File [" + defaultImportFile + "]: " + style.END).strip()
    if not targetSite["importFile"]: targetSite["importFile"] = defaultImportFile

    return targetSite


def getImportData(targetSite):
    defaultImportData = quiverDB + "/imports/" + targetSite["siteName"] + ".sql.gz"
    targetSite["importData"] = input(style.BOLD + "Import Data [" + defaultImportData + "]: " + style.END).strip()
    if not targetSite["importData"]: targetSite["importData"] = defaultImportData

    return targetSite


