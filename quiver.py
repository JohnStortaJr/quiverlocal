#!/usr/bin/python3

from smlib.core import *
from smlib.format import *
from smlib.info import *
from smlib.create import *
from smlib.trust import *
from smlib.delete import *

keepRunning=True

def mainMenu():
    # Run a sudo command to capture the password as soon as the script is run
    #os.system('clear')
    print("")
    print(color.BBLUE + "QuiverLocal WordPress Development Environment Tool " + background.END)
    print(6 * "-" , "OPTIONS" , 6 * "-")
    print(style.NEGATIVE + "1" + style.END + " List Sites")
    print(style.NEGATIVE + "2" + style.END + " New Install")
    print(style.NEGATIVE + "3" + style.END + " Import Site")
    print(style.NEGATIVE + "4" + style.END + " Manage Certificates")
    print(style.NEGATIVE + "5" + style.END + " Delete Site")
    print("")
    print(style.NEGATIVE + "0" + style.END + " Exit")
    print(21 * "-")

    selection = int(getInput("Enter option [0-6]: ", True))

    match selection:
        case 0:
            print("Goodbye")
            return False
        case 1:
            # Display details about installed sites using the info library
            print("Listing Sites")
            getSiteList(quiverDB)
        case 2:
            print("Install New Site")
            createNewSite()
        case 3:
            print("Import Existing Site")
            importSite()
        case 4:
            print("Manage Certificates")
            manageCertificates()
        case 5:
            print("Delete Site")
            deleteSite()
        case _:
            print("")
            print(background.BYELLOW + "Unknown selection" + background.END)
    
    return True
    

def manageCertificates():
    certMenuActive = True
    # Run a sudo command to capture the password as soon as the script is run
    #os.system('clear')

    while certMenuActive:
        print("")
        print(color.BBLUE + "Manage Certificates " + background.END)
        print(6 * "-" , "OPTIONS" , 6 * "-")
        print(style.NEGATIVE + "1" + style.END + " View All Active Certificates")
        print(style.NEGATIVE + "2" + style.END + " Add SSL to an Existing Site")
        print(style.NEGATIVE + "3" + style.END + " Remove SSL from a Site")
        print("")
        print(style.NEGATIVE + "0" + style.END + " Back")
        print(21 * "-")

        selection = int(getInput("Enter option [0-6]: ", True))

        match selection:
            case 0:
                print("Main Menu")
                certMenuActive = False
            case 1:
                # Display details about installed sites using the info library
                print("View All Active Certificates")
                showActiveCertificates()
            case 2:
                print("Add SSL to an Existing Site")
                trustSite()
            case 3:
                print("Remove SSL from a Site")
                untrustSite()
            case _:
                print("")
                print(background.BYELLOW + "Unknown selection" + background.END)         



while keepRunning:
    keepRunning = mainMenu()


