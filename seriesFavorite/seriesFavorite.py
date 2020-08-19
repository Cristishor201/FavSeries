import os, shelve, requests, webbrowser, bs4, re, time, pyautogui
from tkinter import *

# Change the folder of saving

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

    def update(self, opened):
        if self.seasonIn != 0:
            if self.episodeIn + opened > 23:
                self.seasonIn += int((self.episodeIn + opened)/23)
                self.episodeIn = (self.episodeIn + opened) % 23
            else:
                self.episodeIn = self.episodeIn + opened
        else:
            self.episodeIn = self.episodeIn + opened
        self.shelvF[self.title] = [self.seasonIn, self.episodeIn]

    def __del__(self):
        self.shelvF.close()

class UI:
    """User interface of the program."""

    def __init__(self, window, movies): # user interface
        self.movies = movies

        window = window
        window.wm_title(" Filme noi:")
        window.iconbitmap('img/movies.ico')
        window.geometry('370x200')

        Label1 = Label(window, text=movies[0].title, font=("Helvetica", 13))
        Label2 = Label(window, text=movies[1].title, font=("Helvetica", 13))
        Label3 = Label(window, text=movies[2].title, font=("Helvetica", 13))

        self.Slider1 = Scale(window, from_=0, to=movies[0].num, orient=HORIZONTAL, length=250, state=["disabled" if movies[0].num == 0 else "active"])
        self.Slider2 = Scale(window, from_=0, to=movies[1].num, orient=HORIZONTAL, length=250, state=["disabled" if movies[1].num == 0 else "active"])
        self.Slider3 = Scale(window, from_=0, to=movies[2].num, orient=HORIZONTAL, length=250, state=["disabled" if movies[2].num == 0 else "active"])
        self.Slider1.set(movies[0].num)
        self.Slider2.set(movies[1].num)
        self.Slider3.set(movies[2].num)

        Button1 = Button(window, text="CLOSE", width=6, command=window.destroy)
        Button2 = Button(window, text="OPEN", width=7, command=self.opening)

        Label1.grid(row=0, column=0, pady=(10,0), padx=(8,8))
        Label2.grid(row=1, column=0, pady=(10,0), padx=(8,8))
        Label3.grid(row=2, column=0, pady=(10,0), padx=(8,8))
        self.Slider1.grid(row=0, column=1, columnspan=3, pady=(0,5))
        self.Slider2.grid(row=1, column=1, columnspan=3, pady=(0,5))
        self.Slider3.grid(row=2, column=1, columnspan=3, pady=(0,5))
        Button1.grid(row=3, column=0, padx=(10,0), pady=15)
        Button2.grid(row=3, column=3, padx=(0,5), pady=15)

    def opening(self): # open selected movie
        s = [self.Slider1.get(), self.Slider2.get(), self.Slider3.get()]
        if s == [0, 0, 0]:
            return False
        window.destroy()
        for i in range(len(self.movies)):
            for j in range(s[i]):
                webbrowser.open(self.movies[i].links[j], new=0) # open how many movies I want to see once
                time.sleep(1)
        answer = pyautogui.confirm(title="Update movies", text="Do you want to update opened movies ?", buttons=['YES', 'No'])
        if answer == 'OK':
            for item, num in zip(self.movies, s):
                item.update(num)
        else:
            pass

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
    videos=[Boruto, Flash, SuperGirl]

    window = Tk()
    ui = UI(window, videos)
    window.mainloop()
