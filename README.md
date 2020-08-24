Favorite series unseen
===

In short description, it checks if a new episode had appeared, and then let you choose how many you can open in one click for viewing the new one(s).

## Motivation

How would it be if you would not check manually, if it appeared a new episode or more episodes from your favorite series, all done automatically ? Thus it takes your worries about opening same pages, but rather the solicitude of don't loseing some movies. This is how the wish of automation with python it occured.

## Screenshots

In **Screenshot 1** you can select easily how many new episodes want to see from each movie.  
![image](ScreenShoot-1.PNG "ScreenShoot 1")

In **Screenshot 2** you are prompted if you want to update where you have left of watching movies. This is usefull for testing or debuging.  
![image](ScreenShoot-2.PNG "ScreenShoot 2")

## Tech/framework used

**Built with**

   * [Python](https://docs.python.org/3/) ( verssion 3.8.3) running on Windows 7, 64 bit

**Modules used**
   * *os* ......................... -> changing the curent folder of saving shelves dictionary variables
   * *shelve* ................ -> saving informations after I closed the python code
   * *requests*  ............ -> accessing webpage without open it
   * *webbrowser*  ..... -> open webpage
   * *beautifulSoup4* -> parse html
   * *re* ......................... -> take the link for each episode
   * *time* ......................... -> open episodes in order
   * *pyautogui* ................ -> checking for update

## Installation

   1. Make sure before running the main script `seriesFavorite.py` that you run `install.py` firstly. This it will install all required modules for you, and it will create a batch file automatically for you.

## Obtional

If you want this program to run everytime you start / log on on your pc, then ...  
  1. From the `install.py` a new file has been created named `startUp.bat`. Make a shorcut of this file.

  2. On widows os : in `start \ search bar`, type this :
```shell:startup```

  3. Paste the shortcut in this folder.

Done !

### Reset

If you want to reset the episodes from the very begining, run `reset.py`. Warning ! It's not going back after doing this.

## Contributing

If you need to see other movies or series, or if you have ideas of improvement, included how can make this section better, you can open a new issue for that.

Note that requests for xxx movies aren't taken into account, at all. Also minor changes.

## Author
  * Cristian Florescu  - [Cristishor201](https://github.com/Cristishor201)

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE.md](LICENSE) file for details.
