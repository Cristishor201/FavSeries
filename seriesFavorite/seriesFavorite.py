import os, shelve, requests, webbrowser, bs4, re, time, pyautogui, logging
#from tkinter import ttk, Tk, Label, Scale, HORIZONTAL, Button
from tkinter import *

# Change the folder of saving
#os.chdir("C:/Users/Cristian/MyPythonScripts/seriesFavorite") #usefull for running from batch

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

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

    def __init__(self, title, main_url, selectors): # selector=[ serial, episode]
        # take season, episode In
        self.title = title
        self.main_url = main_url
        self.selectors = selectors
        self.shelvF = shelve.open('series')

        if self.title in list(self.shelvF.keys()):
            self.seasonIn, self.episodeIn = self.shelvF[self.title]
        else:
            self.seasonIn, self.episodeIn = self.create()
            logging.error("1", self.seasonIn, self.episodeIn)
            self.shelvF[title] = [self.seasonIn, self.episodeIn]
            logging.error("2", self.shelvF[title])


    @staticmethod
    def arr_start(arr_object): # [Boruto, Naruto, Flash]
        for item in arr_object:
            main_url = item.get_main_url() ; selectors = item.get_selectors()
            episodeIn = item.get_episodeIn() ; forWatching = []
            if len(item.selectors) == 2 :
                seasonIn = item.get_seasonIn() ;
                links = item.crawl(main_url, selectors[0])
                seasonMax = len(links)
                first = True
                for i in range(seasonIn-1, seasonMax):
                    if first:
                        episode = item.crawl(links[i], selectors[1])[::-1][(episodeIn-1):]
                        first = False
                    else:
                        episode = item.crawl(links[i], selectors[1])[::-1]
                    forWatching.extend(episode)
                item.set_links(forWatching) ; item.set_num(len(forWatching))

            elif len(item.selectors) == 1:
                episode = item.crawl(main_url, selectors[0])[::-1][(episodeIn +1):-1]
                forWatching.extend(episode)
                item.set_links(forWatching) ; item.set_num(len(forWatching))

            else:
                raise Exception("Error - too more or none selectors")

    @staticmethod
    def crawl(url, selector):
        result = []
        res = requests.get(url)
        res.raise_for_status()
        selectAllLink = selector
        page = bs4.BeautifulSoup(res.text, 'html.parser')
        elements = page.select(selectAllLink)
        regexUrl = re.compile(r'''
        # https://divxfilmeonline.org/the-flash-sezonul-5-episodul-13/
        (href=")    #start part
        ([\w:/.-]+)
        (")         # end part
        ''', re.VERBOSE)
        for i in range(len(elements)):
            url = regexUrl.search(str(elements[i]))
            result.append(url.group(2))
        return result

    def set_num(self, num):
        self.num = num

    def set_links(self, links):
        self.links = links

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
        logging.info("4", opened)
        if self.seasonIn != 0:
            logging.warning("5", self.episodeIn)
            if self.episodeIn + opened > 23:
                self.seasonIn += int((self.episodeIn + opened)/23)
                self.episodeIn = (self.episodeIn + opened) % 23
            else:
                self.episodeIn = self.episodeIn + opened
        else:
            self.episodeIn = self.episodeIn + opened
        logging.critical("6", self.seasonIn, self.episodeIn)
        self.shelvF[self.title] = [self.seasonIn, self.episodeIn]

    def get_main_url(self):
        return self.main_url

    def get_selectors(self):
        return self.selectors

    def get_seasonIn(self):
        return self.seasonIn

    def get_episodeIn(self):
        return self.episodeIn

    def __del__(self):
        self.shelvF.close()

class UI:
    """User interface of the program."""

    def __init__(self, window, movies): # user interface
        self.movies = movies
        self.sliders = []
        self.window = window

        window.wm_title(" Filme noi:")
        window.iconbitmap('img/movies.ico')
        window.geometry('370x220')

        frame1 = Frame(window, width=370)
        frame2= Frame(window, height=50)

        window.grid_rowconfigure(0, weight=3)
        window.grid_rowconfigure(1, weight=1)
        frame2.grid_columnconfigure(1, weight=1)

        frame1.grid(row=0, sticky="nsew")
        frame2.grid(row=1, sticky="nsew")

        #scroll
        mycanvas = Canvas(frame1, bg="blue")
        mycanvas.grid_rowconfigure(0, weight=1)
        mycanvas.grid(row=0, column=0, sticky="nsew")

        myScrollBar = Scrollbar(frame1, orient=VERTICAL, command=mycanvas.yview)
        myScrollBar.grid(row= 0, column= 0)

        mycanvas.configure(yscrollcommand=myScrollBar.set)
        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

        frame_scrollable = Frame(mycanvas)

        mycanvas.create_window((0,0), window=frame_scrollable, anchor="nw")

        if len(movies) > 3:
            print("scroll")
            #main_window(window) #schimb self.window
        else:
            print("normal")

        for i in range(len(movies)):
            Labelt = Label(frame_scrollable, text=movies[i].title, font=("Helvetica", 13))
            Labelt.grid(row=i, column=0, pady=(10,0), padx=(8,8))

            Slider = Scale(frame_scrollable, from_=0, to=movies[i].num, orient=HORIZONTAL, length=250, state=["disabled" if movies[i].num == 0 else "active"])
            Slider.set(movies[i].num)
            Slider.grid(row=i, column=1, columnspan=3, pady=(0,5))
            self.sliders.append(Slider)

        Button1 = Button(frame2, text="CLOSE", width=6, command=window.destroy)
        Button2 = Button(frame2, text="OPEN", width=7, command=self.opening)

        Button1.grid(row=0, column=0, padx=(25,0), pady=15, sticky="w")
        Button2.grid(row=0, column=3, padx=(0,35), pady=15, sticky="e")
        
    def opening(self): ######### open selected movie
        s = [] # values with selected in sliders
        count = 0
        for i in range(len(self.sliders)):
            item = self.sliders[i].get()
            if item == 0:
                count+=1
            s.append(item)

        if count == i + 1: # if all are zeros exit
            print("all are zeros")
            return False
        window.destroy()

        for i in range(len(self.movies)):
            for j in range(s[i]):
                webbrowser.open(self.movies[i].links[j], new=0) # open how many movies I want to see once
                time.sleep(1)
        answer = pyautogui.confirm(title="Update movies", text="Do you want to update opened movies ?", buttons=['YES', 'No'])
        if answer == 'YES':
            for item, num in zip(self.movies, s):
                logging.info("3", item, num)
                item.update(num)

if __name__ == '__main__':
    Boruto = Movie('Boruto', 'https://www.naruget.tv/category/boruto-subbed/', ["div.c50 > div.eptit > a",])

    """Flash = Movie('Flash',
    'https://divxfilmeonline.org/seriale-online/the-flash/',
    ["li.border-radius-5 a",
    "ul.listing-videos li a"])
    """

    videos=[Boruto, Boruto, Boruto, Boruto, Boruto]
    Movie.arr_start(videos)

    window = Tk()
    ui = UI(window, videos)
    window.mainloop()
