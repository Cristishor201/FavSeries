import os, re, pyautogui

# edit the abs path of saving
path = os.getcwd()
with open("seriesFavorite.py", "r") as r:
    lines = r.read().split('\n')
    line = lines[4]
    parts = re.split("([\('\)]+)", line)
    new_line = ''.join(parts[:2] + [path] + parts[3:])

with open("seriesFavorite.py", "w") as w:
    w.write('\n'.join(lines[:4] + [new_line] + lines[5:]))

response = pyautogui.confirm(title="Bat file", text="Do you want to create a bat file and for running the script at every start up ?", buttons=["YES", "No"])
if response == "YES":
    with open("startUp.bat", 'w') as s:
        text = "@py " + path + "\seriesFavorite.py\n@pause"
        s.write(text)
