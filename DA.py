
import requests,json,random
class DiscogsAgent:
    _userPage = {}
    _user = ''

    def __init__(self,user):
        DiscogsAgent._user = user
        user_agent = {'User-agent':'silt/0.1'}
        discogsURL = 'https://api.discogs.com/users/{}'.format(DiscogsAgent._user)
        r = requests.get(discogsURL, headers = user_agent)
        DiscogsAgent._userPage = r.json()

    def dictUser(self):
        return DiscogsAgent._userPage

    def curUser(self):
        return DiscogsAgent._user


