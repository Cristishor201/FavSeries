import os, shelve, requests, webbrowser, bs4, re

# Change the folder of saving
os.chdir('C:\\Users\\Cristian\\MyPythonScripts\\seriesFavorite')

class Movie:
    def __init__(self, title, url, selectors):
        # take season, episode In
        self.title = title
        shelvF = shelve.open('series')
        self.seasonIn, self.episodeIn = shelvF[title]
        shelvF.close()

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
        num = 0 ; first = 0
        selectAllEpsodes = selectors[1]
        for season in range(self.seasonIn, self.seasonMax+1):
            ep = [] # list of episodes found
            episodeRes = requests.get(selectors[2] + str(season) + '/')
            episodeRes.raise_for_status()
            page = bs4.BeautifulSoup(episodeRes.text, 'html.parser') # page 2 - episodes
            elements = page.select(selectAllEpsodes)
            regexUrl = re.compile(r'''
            # https://divxfilmeonline.org/the-flash-sezonul-5-episodul-13/
            (href=")    #start part
            ([\w:/.-]+)
            (")         # end part
            ''', re.VERBOSE)
            


    def open(): # open selected movie
        pass

    def update(self):
        # iau titlu din title, si adaug un atribut de nr. deschise -> fac automat la update
        pass

    def ui(): # user interface
        pass

if __name__ == '__main__':
    #Boruto = Movie('Boruto')
    Flash = Movie('Flash',
    'https://divxfilmeonline.org/seriale-online/the-flash/',
    ['ul.listing-cat span', # for getting season max
    '#content > ul.listing-videos.listing-tube > li a', # select all episodes
    'https://divxfilmeonline.org/seriale-online/the-flash/the-flash-sezonul-']) # link per season
    #SuperGirl = Movie('SuperGirl')
