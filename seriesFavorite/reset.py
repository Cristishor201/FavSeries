import shelve, pyautogui

response = pyautogui.confirm(title="Reset series", text="Are you sure you want to reset ?", buttons=["YES", "No"])
if response == "YES":
    shelvF = shelve.open("series")
    for title in list(shelvF.keys()):
        if shelvF[title][0] == 0:
            shelvF[title] = [0, 1]
        else:
            shelvF[title] = [1, 1]

    shelvF.close()
