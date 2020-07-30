import os, shelve, requests, webbrowser, bs4, re
from tkinter import *
from PIL import ImageTk, Image

#window = Tk()

# Change the folder of saving
os.chdir('seriesFavorite')

class Movie:
    """Look up for favorite serials :)
    ====================================
    Require:

    title = String named by you only once
    url = url with all episodes / seasons
    selectors = list of:
    - season css selector
    - episode css selector
    - incomplete link of a season
    """

    def __init__(self, title, url, selectors):
        # take season, episode In
        self.title = title
        self.shelvF = shelve.open('series')
        if self.title in list(self.shelvF.keys()):
            self.seasonIn, self.episodeIn = self.shelvF[title]
        else:
            self.seasonIn, self.episodeIn = self.create()
            self.shelvF[title] = [self.seasonIn, self.episodeIn]

        if self.seasonIn != 0:
            # link sesons -> take seasonMax
            seasonRes = requests.get(url)
            seasonRes.raise_for_status()
            selectAllTitles = selectors[0]
            page = bs4.BeautifulSoup(seasonRes.text, 'html.parser') # seasons
            elements = page.select(selectAllTitles) # list of all elems
            text = elements[-1].text
            seasonMax = int(text[-2:].strip())
            self.seasonMax = seasonMax
        else:
            self.seasonMax = 0

        #  for -> for - save all the links in list finding
        num = 0 ; first = 0 ; self.links = []
        selectAllEpsodes = selectors[1]
        for season in range(self.seasonIn, self.seasonMax+1):
            ep = [] # list of episodes found
            if self.seasonIn !=0:
                episodeRes = requests.get(selectors[2] + str(season) + '/')
            else:
                episodeRes = requests.get(url)
            episodeRes.raise_for_status()
            page = bs4.BeautifulSoup(episodeRes.text, 'html.parser')
            elements = page.select(selectAllEpsodes)

            regexUrl = re.compile(r'''
            # https://divxfilmeonline.org/the-flash-sezonul-5-episodul-13/
            (href=")    #start part
            ([\w:/.-]+)
            (")         # end part
            ''', re.VERBOSE)
            if(first == 0):
                begin = self.episodeIn -1 # substract episodes viewed
                first += 1
            else:
                begin = 0
            #print("first: ", first,"begin: ", begin)

            for episode in range(0, len(elements) - begin):
                url = regexUrl.search(str(elements[episode]))
                num += 1
                ep.insert(0, url.group(2)) # per episode

            self.links.extend(ep) # add season of episode links
        self.num = num


    def _reset(self):
        print("[seasonIn, episodeIn]", [self.seasonIn, self.episodeIn])
        self.shelvF[self.title] = [1, 1]

    def _update(self, movies=[1, 1]):
        self.shelvF[self.title] = movies

    def _delete_item(self):
        del self.shelvF[self.title]
        print("delete succesefully")

    def _debug(self):
        print("keys-", list(self.shelvF.keys()))
        print("values-", list(self.shelvF.values()))

    def create(self):
        try:
            serial = int(input("{}- Pune numarul serialului la care ai ramas de vazut \n(0 - daca nu are seriale): ".format(self.title)))
            episode = int(input("{}- Pune numarul episodului la care ai ramas de vazut: ".format(self.title)))
        except:
            raise Exception("Doar numere intregi!")
        return [serial, episode]

    def open(): # open selected movie
        pass

    def update(self):
        # iau titlu din title, si adaug un atribut de nr. deschise -> fac automat la update
        pass

    @staticmethod
    def ui(window): # user interface
        Movie.window = window
        Movie.window.wm_title(" Filme noi:")
        Movie.window.iconbitmap('img/movie.ico')
        Movie.window.geometry('400x300')


    def __del__(self):
        self.shelvF.close()
        window

if __name__ == '__main__':
    Boruto = Movie('Boruto',
    'https://narutotubes.com/boruto-naruto-next-generations-eng-sub/',
    ["___",
    '#post-2579 > .entry-content > ul.display-posts-listing > .listing-item a',
    "___"]
    )
    Flash = Movie('Flash',
    'https://divxfilmeonline.org/seriale-online/the-flash/',
    ['ul.listing-cat span', # for getting season max
    '#content > ul.listing-videos.listing-tube > li a', # select all episodes
    'https://divxfilmeonline.org/seriale-online/the-flash/the-flash-sezonul-']) # link per season
    SuperGirl = Movie('SuperGirl',
    "https://divxfilmeonline.org/seriale-online/supergirl/",
    ['ul.listing-cat span',
    '#content > ul.listing-videos.listing-tube > li a',
    'https://divxfilmeonline.org/seriale-online/supergirl/supergirl-sezonul-'])

    window = Tk()
    Boruto.ui(window)
    window.mainloop()

    """movies = [Boruto, Flash, SuperGirl]
    for item in movies:
        print(item.links, item.num)"""
