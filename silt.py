#!/usr/bin/env python3

import requests,json,random
from sys import argv
import os
import configparser


"""
pulling from discogs whether or not the user exists
"""
def discogsPull(user):
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

"""
the user must be valid, parsing through data and populating a list of their collection
if we were successfully able to pull all of this information, open a new config and write that username to file 
"""
def getRandom(library,libraryKeys):
    random.seed()
    listenTo = libraryKeys[random.randrange(len(library))]
    return listenTo

def popLibrary(user):
    if discogsPull(user) != False:
        library, libraryKeys = discogsPull(user)
        listenTo = getRandom(library,libraryKeys)
        print('\nYou should listen to:\n'+listenTo,'by',library[listenTo])
        no = input('\n\nAnother?')
        while no.lower() != 'n' and no.lower() != 'no':
            listenTo = libraryKeys[random.randrange(len(library))]
            print('\nHow about...\n'+listenTo,'by',library[listenTo])
            no = input('\n\nAnother?')
    else:
        print('Invalid User.')
        user = input('Enter discogs username:')
        popLibrary(user)

"""
checking for arguments
"""
if len(argv) > 1:
    if '-u' in argv and argv.index('-u') + 1 < len(argv):
        user = argv[argv.index('-u') + 1]
    elif not argv.index('-u') + 1 < len(argv):
        user = input('Enter discogs username:')
else: 
    user = input('Enter discogs username:')

popLibrary(user)
