#!/usr/bin/env python3

import requests,json,random
from sys import argv
from os import getenv
import configparser


def help():
    """
    argument help statement
    """
    print('\nsilt: discogs recommendations for the command line why not')
    print('Usage:')
    # print("silt [-u 'username'] [-c 'non-default config']")
    print("silt [-r #] [-u 'username']")
    print("-r: number of recommendations. Default = 1")
    print("-u: username")

def discogsPull(user):
    """
    pulling from discogs whether or not the user exists
    """
    user_agent = {'User-agent':'silt/0.0'}
    discogsURL = 'https://api.discogs.com/users/{}/collection/folders/0/releases'.format(user)
    r = requests.get(discogsURL, headers = user_agent)
    discogsDictAll = r.json()
    if 'message' in discogsDictAll:
        return False
    else:
        library = {}
        for release in discogsDictAll['releases']:
            for info in release:
                if type(release[info])== dict:
                    library[release[info]['title']] = release[info]['artists'][0]['name']
        libraryKeys = list(library)
        return library, libraryKeys

def getRandom(recAmt,library,libraryKeys):
    """
    the user must be valid, parsing through data and populating a list of their collection
    if we were successfully able to pull all of this information, open a new config and write that username to file 
    """
    random.seed()
    listenTo = []
    for ct in range(recAmt):
        tempRec = libraryKeys[random.randrange(len(library))]
        tempStr = tempRec+' by '+library[tempRec]
        if tempStr not in listenTo:
            listenTo.append(tempStr)
        else:
            ct += 1
    return listenTo

def popLibrary(user,recAmt):
    """
    does the heavy lifting, interprates discogsPull and prints the recommendations.
    """
    if discogsPull(user) != False:
        library, libraryKeys = discogsPull(user)
        listenTo = getRandom(recAmt,library,libraryKeys)
        print('\nYou should listen to:\n')
        for rec in listenTo:
            print(rec)
        # for ct in range(0,recAmt):
        #     print(listenTo,'by',library[listenTo])
        #     listenTo = getRandom(library,libraryKeys)

    else:
        print('Invalid User "{}".'.format(user))
        user = input('Enter discogs username:')
        popLibrary(user)

# def configParse(toParse):
    


home = getenv("HOME") # defining home folder
config = configparser.ConfigParser() #initializing config parser object
config.read('{}/.config/silt.ini'.format(home)) #sending default config file to config parser object

"""
main-ish
interprates arguments and decides what to do depending on what arguments are provided
too messy, I'd like to clean this up
"""
if len(argv) > 1:
    if '-u' in argv:
        if argv.index('-u') + 1 < len(argv):
            user = argv[argv.index('-u') + 1]
        elif not argv.index('-u') + 1 < len(argv):
            print('Incorrect formatting for "-u" argument. We need something after it.')
            user = input('Enter discogs username:')
    elif '-u' not in argv:
        if 'user' in config['default']:
            user = config['default']['user']
        else:
            user = input('Enter discogs username:')

    if '-r' in argv:
        if argv.index('-r') + 1 < len(argv):
            try:
                int(argv[argv.index('-r') + 1])
                recAmt = int(argv[argv.index('-r') + 1])
            except (TypeError,ValueError):
                print('Incorrect formatting for "-r" argument. We need an integer after it.')
                help()
                recAmt = 0
        else:
            help()
    else:
        if 'user' in config['default']:
            user = config['default']['user']
        else:
            user = input('Enter discogs username:')
        help()

else: 
    recAmt = 1
    if 'recAmt' in config['default']:
        recAmt = config['default']
    else:
        recAmt = 1

    if 'user' in config['default']:
        user = config['default']['user']
    else:
        user = input('Enter discogs username:')

popLibrary(user,recAmt)
