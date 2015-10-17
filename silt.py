#!/usr/bin/env python3

import requests,json,random
from sys import argv
from os import getenv
from os import path
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
        return library

def genSuggest(recAmt,library,libraryKeys):
    """
    the user must be valid, parsing through data and populating a list of their collection
    if we were successfully able to pull all of this information, open a new config and write that username to file 
    """
    random.seed()
    listenList = []
    for ct in range(recAmt):
        tempRec = libraryKeys[random.randrange(len(library))]
        tempStr = tempRec+' by '+library[tempRec]
        if tempStr not in listenList:
            listenList.append(tempStr)
        else:
            ct += 1
    return listenList


def popLibrary(user):
    """
    does the heavy lifting, interprates discogsPull and prints the recommendations.
    """
    if discogsPull(user) != False:
        library = discogsPull(user)
        return library

    else:
        print('Invalid User "{}".'.format(user))
        user = input('Enter discogs username:')
        popLibrary(user)

    
def configParse():
    home = getenv("HOME") # defining home folder
    config = configparser.ConfigParser() #initializing config parser object
    config.read('{}/.silt/silt.ini'.format(home)) #sending default config file to config parser object
    user,recAmt,library,libraryFile = None,None,None,None
    if 'user' in config['default']:
        user = config['default']['user']
    if 'recAmt' in config['default']:
        try:
            recAmt = int(config['default']['recAmt'])
        except (TypeError,ValueError):
            recAmt = None
    if 'libraryFile' in config['default']:
        libraryFile = config['default']['libraryFile']
        libraryFile = path.expanduser(libraryFile)
        library = libraryFromFile(libraryFile)
    elif 'libraryFile' not in config['default']:
        libraryFile = '{}/.silt/libraryFile.json'.format(home)

    return user,recAmt,library,libraryFile

def libraryFromFile(libraryFile):
    try:
        with open(libraryFile,'r') as database:
            library = json.load(database)
            return library

    except ( FileNotFoundError ):
        return None


def libraryDump(library,libraryFile):
    try:
        with open(libraryFile,'w+') as database:
            json.dump(library,database)
    except:
        home = getenv("HOME")
        libraryFile = '{}/.silt/libraryFile.json'.format(home)
        with open(libraryFile,'w+') as database:
            json.dump(library,database)


def main():
    user,recAmt,library,libraryFile = configParse()
    if library == None:
        if user == None:
            user = input('Enter discogs username:')
    if recAmt == None:
        recAmt = 1

    """
    main-ish
    interprates arguments and decides what to do depending on what arguments are provided
    too messy, I'd like to clean this up
    """
    validArgs = ['-u','-r','-h','-update']
    if len(argv) > 1:
        if '-u' in argv:
            if argv.index('-u') + 1 < len(argv):
                user = argv[argv.index('-u') + 1]
                library = popLibrary(user)
            elif not argv.index('-u') + 1 < len(argv): # no username given
                print('Incorrect formatting for "-u" argument. We need a number after it.')
                user = input('Enter discogs username:')

        if '-r' in argv:
            if argv.index('-r') + 1 < len(argv):
                try:
                    int(argv[argv.index('-r') + 1])
                    recAmt = int(argv[argv.index('-r') + 1])

                except (TypeError,ValueError):
                    print('Incorrect formatting for "-r" argument. We need an integer after it. Defaulting to 1')
                    help()
                    recAmt = 1
            else:
                print("Incorrect formatting for "-r" argument. We need a number after it.")
                recAmt = 1
                help()

        if '-h' in argv:
            help()

        if '-update' in argv:
            print('Updating...')
            library = popLibrary(user)
            libraryDump(library,libraryFile)

        if '-u' not in argv and '-r' not in argv and '-update' not in argv: # some argument was given but not valid
            help()

    if library == None:
        library = popLibrary(user)
        libraryDump(library,libraryFile)
        listenList = genSuggest(recAmt,library,list(library))
        print('\nYou should listen to:\n')
        for rec in listenList:
            print(rec)

    else:
        listenList = genSuggest(recAmt,library,list(library))
        print('\nYou should listen to:\n')
        for rec in listenList:
            print(rec)

try:
    main()
except KeyboardInterrupt:
    pass
