#!/usr/bin/python3

import os

def initializeValues():
    quiverHome = os.getcwd()
    quiverDB = quiverHome + "/sitedb"

    user = os.path.expanduser('~')
    userHome = os.getenv("HOME")

    certHome = userHome + "/certificates"
    exportHome = userHome + "/exports"
    importFile = exportHome + "/NOFILE"
    importData = exportHome + "/NODATA"

    domainHome = userHome + "/domains"
    domainConfig = domainHome + "/config"

    apacheRoot = "/etc/apache2"
    apacheConf = apacheRoot + "/sites-available"
    apacheLog = "var/log/apache2"

    siteName = "localdev01"
    domainName = siteName + ".local"

    dbName = siteName + "_db"
    dbUser = "wordpress"
    dbPass = "start123"

    certName = "myCert"
    certDuration = 365
    certKeyFile = certHome + "/localcert.key"
    certFile = certHome + "/localcert.crt"