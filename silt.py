#!/usr/bin/env python3

import requests,json,random
random.seed()
user = input('Enter discogs username:')
user_agent = {'User-agent':'silt/0.0'}
discogsURL = 'https://api.discogs.com/users/{}/collection/folders/0/releases'.format(user)
r = requests.get(discogsURL, headers = user_agent)
discogsDictAll = r.json()
library = {}
for i in discogsDictAll['releases']:
    for e in i:
        # print(i[e])
        if type(i[e])== dict:
            library[i[e]['title']] = i[e]['artists'][0]['name']
libraryKeys = list(library)
listenTo = libraryKeys[random.randrange(len(library))]
while True:
    print('You should listen to:\n'+listenTo,'by',library[listenTo])
    input('\n\nAnother?')
    listenTo = libraryKeys[random.randrange(len(library))]
