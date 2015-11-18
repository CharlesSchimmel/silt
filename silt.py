#!/usr/bin/env python3

import requests,json,random,shutil
from sys import argv
from os import getenv
from os import path
import configparser
from gi.repository import Gtk

class mainWin(Gtk.Window):
    def __init__(self,user,library):
        self.library = library
        self.curRec = ranSuggest(self.library)
        Gtk.Window.__init__(self,title="Silt")

        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.set_border_width(5)

        labelText = "How about:"
        self.label1 = Gtk.Label()
        self.label1.set_markup("How about:")
        self.grid.attach(self.label1,0,0,1,1)
        self.label1.set_hexpand(True)

        self.recLabel = Gtk.Label()
        tmpText = "<b>{}</b>".format(ranSuggest(self.library))
        self.recLabel.set_markup(tmpText)
        self.grid.attach(self.recLabel,0,1,1,1)
        self.recLabel.set_hexpand(True)

        self.cover = Gtk.Frame()
        self.grid.attach(self.cover,0,2,1,1)
        self.img = Gtk.Image.new_from_file('')
        self.cover.add(self.img)

        self.anotherButton = Gtk.Button(label="Another")
        self.anotherButton.connect("clicked",self.newRec)
        self.anotherButton.connect("clicked",self.updateImage)
        self.grid.attach(self.anotherButton,0,3,1,1)
        self.anotherButton.set_hexpand(True)

        # Who needs an exit button? Everybody's got window controls...
        # self.closeButton = Gtk.Button(label="Exit")
        # self.grid.attach(self.closeButton,0,4,1,1)
        # self.closeButton.connect("clicked",self.close)
        # self.closeButton.set_hexpand(True)
        
        self.grabImages()
        self.img.set_from_file('/tmp/image.jpg')


    # def close(self,widget):
    #     Gtk.main_quit()

    def newRec(self,widget):
        self.curRec = ranSuggest(self.library)
        tmpText = "<b>{}</b>".format(self.curRec)
        self.recLabel.set_markup(tmpText)

    def updateImage(self,widget):
        self.grabImages()
        self.img.set_from_file('/tmp/image.jpg')

    def grabImages(self):
        headers = {'user-agent':'silt/0.1 +https://github.com/charlesschimmel/silt','Authorization':'Discogs key=JwTFBZkshygrKQlbltem,secret=oAKieUZtUMLBQJDryTlxEMnQFzPhCyJx'}
        releaseURL = self.library[self.curRec]
        r = requests.get(releaseURL,headers=headers)
        if r.status_code == 200:
            r = r.json()
            if 'images' in sub:
                for sub in r['images']:
                    if sub['type'] == 'primary':
                        r = requests.get(sub['resource_url'],headers=headers, stream=True)
                        with open('/tmp/image.jpg','wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw,f)
            else:
                print('No image available for this release.')
        else:
            pass

"""
TODO: make a "no connection available" window
class noConWin(Gtk.Window):
    def __init__(self,user,library)
"""

        



def help():
    """
    argument help statement
    print("-u: username")
    """
    print('\nsilt: discogs recommendations for the command line why not')
    print('Usage:')
    # print("silt [-u 'username'] [-c 'non-default config']")
    print("silt [-r #] [-update]")
    print("-r: number of recommendations. Default = 1")
    print("-update: update local library")

def discogsPull(user):
    """
    pulling from discogs whether or not the user exists
    """
    headers = {'user-agent':'silt/0.1 +https://github.com/charlesschimmel/silt','Authorization':'Discogs key=JwTFBZkshygrKQlbltem,secret=oAKieUZtUMLBQJDryTlxEMnQFzPhCyJx'}
    discogsURL = 'https://api.discogs.com/users/{}/collection/folders/0/releases'.format(user)
    r = requests.get(discogsURL, headers=headers)
    discogsDictAll = r.json()

    if 'message' in discogsDictAll:
        return False
    elif r.status_code != 200:
        return False
    else:
        library = {}
        for release in discogsDictAll['releases']:
            library[release['basic_information']['title']] = release['basic_information']['resource_url']
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
        tempStr = tempRec
        if tempStr not in listenList:
            listenList.append(tempStr)
        else:
            ct += 1
    return listenList

def ranSuggest(library):
    random.seed()
    tempRec = list(library.keys())[random.randrange(len(library))]
    return tempRec
        

def popLibrary(user):
    """
    does the heavy lifting, interprates discogsPull and prints the recommendations.
    """
    if discogsPull(user) != False:
        library = discogsPull(user)
        return library

    elif not discogsPull(user):
        print('Invalid User "{}".'.format(user))
        popLibrary(input('Enter discogs username: '))

    
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

    except(OSError,IOError):
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
    validArgs = ['-r','-h','-update']
    if len(argv) > 1:
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
            print('Done.')

        if '-r' not in argv and '-update' not in argv and '-gtk' not in argv: # some argument was given but not valid
            help()


    if '-update' not in argv and '-h' not in argv:
        if library == None:
            library = popLibrary(user)
            libraryDump(library,libraryFile)
            listenList = genSuggest(recAmt,library,list(library))
            if '-gtk' in argv:
                mainGtk(user,library)
            else:
                mainCli(listenList)

        else:
            listenList = genSuggest(recAmt,library,list(library))
            if '-gtk' in argv:
                mainGtk(user,library)
            else:
                mainCli(listenList)

def mainGtk(user,library):
    win = mainWin(user,library)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

def mainCli(listenList):
    print('\nYou should listen to:\n')
    for rec in listenList:
        print(rec)
try:
    main()

except KeyboardInterrupt:
    pass
