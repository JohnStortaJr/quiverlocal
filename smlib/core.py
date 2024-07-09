#!/usr/bin/python3

import os

# Quiver directories
quiverHome = os.getcwd()
quiverDB = quiverHome + "/sitedb/"

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

