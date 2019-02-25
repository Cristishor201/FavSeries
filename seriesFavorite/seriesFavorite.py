# Favorite serials: Flash, Boruto
seriesFavorite = ['Flash', 'Boruto']
finding = { 'Flash': [], 'Boruto': []}
import os, shelve, requests, webbrowser, bs4, re

# Change the folder of saving
os.chdir('C:\\Users\\Cristian\\MyPythonScripts\\seriesFavorite')

def Flash(movie): # Flash function
    # take season, episode In
    seasonIn, EpisodeIn = takeDatabase(movie)
    
    # link sesons -> take seasonMax
    seasonRes = requests.get('https://divxfilmeonline.org/seriale-online/the-flash/')
    seasonRes.raise_for_status()
    selectAllTitles = 'ul.listing-cat > li.border-radius-5.box-shadow > a:nth-child(2) > span'
        
    page1 = bs4.BeautifulSoup(seasonRes.text, 'html.parser') # page 1 - seasons
    elements = page1.select(selectAllTitles) # list of all elems
    text1 = elements[-1].text
    seasonMax = int(text1[-2:].strip())

    # for -> for -> save all the links in list finding
    num = 0 ; first = 0
    selectAllA = '#content > ul.listing-videos.listing-tube > li a'
    for season in range(seasonIn, seasonMax+1):
        ep = [] # list of episodes found
        episodeRes = requests.get('https://divxfilmeonline.org/seriale-online/the-flash/the-flash-sezonul-' + str(season) + '/')
        episodeRes.raise_for_status()
        page2 = bs4.BeautifulSoup(episodeRes.text, 'html.parser') # page 2 - episodes
        elements2 = page2.select(selectAllA)
        regexUrl = re.compile(r'''
        # https://divxfilmeonline.org/the-flash-sezonul-5-episodul-13/
        (href=")    #start part
        ([\w:/.-]+)
        (")         # end part
        ''', re.VERBOSE)
        if(first == 0):
            begin = EpisodeIn -1 # substract episodes viewed
            first += 1
        else:
            begin = 0
        
        for episode in range(0, len(elements2) - begin):
            url = regexUrl.search(str(elements2[episode]))
            num += 1
            ep.insert(0, url.group(2)) # per episode

        finding['Flash'].extend(ep) # add season of episode links
 
    # if none has been found -> return 0 | else return num of episodes
    return num

def Boruto(movie): # Boruto function
    # take episode in
    EpisodeIn = takeDatabase(movie)
    
    # link list of movie -> for -> save (\>) in the list (<-) finding
    num = 0 ; ep = []
    selectAllA = '#post-2579 > .entry-content > ul.display-posts-listing > .listing-item a'
    episodeRes = requests.get('https://narutotubes.com/boruto-naruto-next-generations-eng-sub/')
    episodeRes.raise_for_status()
    page = bs4.BeautifulSoup(episodeRes.text, 'html.parser') # page - episodes
    elements = page.select(selectAllA)
    regexUrl = re.compile(r'''
        # https://narutotubes.com/boruto-94-episode-english-subbed-a-heaping-helping-the-eating-contest/
        (href=")    #start part
        ([\w:/.-]+)
        (")         # end part
        ''', re.VERBOSE)
    for episode in range(0, len(elements) - EpisodeIn+1):
        url = regexUrl.search(str(elements[episode]))
        num += 1
        ep.insert(0, url.group(2))
    finding['Boruto'] = ep
    # if none has been found -> return 0 | else return num of new episode
    return num

def takeDatabase(movie): # Take infos from old movies
    shelvF = shelve.open('series')

    if(movie == 'Flash'):
        season, episode = shelvF['Flash']
        shelvF.close()
        return [season, episode] # list of int
    elif(movie == 'Boruto'):
        episode = shelvF['Boruto']
        shelvF.close()
        return episode           # int

def updateDatabase(movie, opened): # Update old movies
    shelvF = shelve.open('series', 'w')
    
    if(movie == 'Flash'):
        season, episode = takeDatabase(movie)
        
        if(episode + opened > 23):
            season += int((episode + opened)/ 23)
            episode = (episode + opened) % 23
        else:
            episode = episode + opened
        shelvF['Flash'] = [season, episode] # update next season, episode
    elif(movie == 'Boruto'):
        episode = takeDatabase(movie)
        shelvF['Boruto'] = episode + opened
        
    shelvF.close()

for i in range(len(seriesFavorite)):
    if(seriesFavorite[i] == 'Flash'):
        movieNum = Flash(seriesFavorite[i])
    elif(seriesFavorite[i] == 'Boruto'):
        movieNum = Boruto(seriesFavorite[i])

    if(movieNum == 0):
        print("\nDidn't appeared any new episode from " + seriesFavorite[i] + '.')
    else:
        print('\nI found ' + str(movieNum) + ' new episode(s) from ' + seriesFavorite[i])
        try:
            display = int(input('How many you want to open ? (0, 1, 2...)\n'))
        except:
            raise Exception('Only integer numbers allowed !')
        if(display < 0):
            raise Exception("You can't open negative new movies.")
        if(display > movieNum):
            raise Exception("You can't open more new movies, than they already appeared.")
    
        if(display == 0):
            pass
        else: # if I want to open some num of movies
            for j in range(0, display):
                webbrowser.open(finding[seriesFavorite[i]][j], new=0) # open how many movies I want to see once
        updateDatabase(seriesFavorite[i], display)
        movieNum = 0 # back to none
        display = 0
