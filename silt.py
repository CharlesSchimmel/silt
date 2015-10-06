#!/usr/bin/env python3

import requests,json,random
from sys import argv
import os

if os.path.isfile('silt.conf'):
    discogsFile = open('silt.conf','r+')
elif not os.path.isfile('silt.conf'):
    discogsFile = open('silt.conf','w+')
discogsList = discogsFile.readlines()


if len(argv) > 1:
    if '-u' in argv:
        argUser = argv[argv.index('-u') + 1]
        user = argUser
else: 
    if len(discogsList) > 0:
        user = discogsList[0][5:]
        print('Retrieving Discogs information for:',user,'\n\n')
    elif len(discogsList) == 0:
        user = input('Enter discogs username:')
        toWrite = 'user='+user
        discogsFile.write(toWrite);

discogsFile.close()

random.seed()
user_agent = {'User-agent':'silt/0.0'}
discogsURL = 'https://api.discogs.com/users/{}/collection/folders/0/releases'.format(user)
r = requests.get(discogsURL, headers = user_agent)
discogsDictAll = r.json()

if 'message' in discogsDictAll:
    print('\nUser not found.')
else:
    library = {}
    for i in discogsDictAll['releases']:
        for e in i:
            # print(i[e])
            if type(i[e])== dict:
                library[i[e]['title']] = i[e]['artists'][0]['name']

    libraryKeys = list(library)
    listenTo = libraryKeys[random.randrange(len(library))]
    print('\nYou should listen to:\n'+listenTo,'by',library[listenTo])
    no = input('\n\nAnother?')
    while no.lower() != 'n' and no.lower() != 'no':
        listenTo = libraryKeys[random.randrange(len(library))]
        print('\nHow about...\n'+listenTo,'by',library[listenTo])
        no = input('\n\nAnother?')
    discogsFile.close()
    discogsFile = open('silt.conf','w+')
    toWrite = 'user='+user
    discogsFile.write(toWrite);
