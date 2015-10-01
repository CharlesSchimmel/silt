#!/usr/bin/env python3

import requests,json,random
user_agent = {'User-agent':'wSilt/0.0'}
r = requests.get('https://api.discogs.com/users/calchuchesta/collection/folders/0/releases', headers = user_agent)
discogsDictAll = r.json()
library = []
for i in discogsDictAll['releases']:
    for e in i:
        # print(i[e])
        if type(i[e])== dict:
            library.append((i[e]['title'],'by',i[e]['artists'][0]['name']))
random.seed()
listenTo = random.randrange(len(library))
print('You should listen to:',library[listenTo])
