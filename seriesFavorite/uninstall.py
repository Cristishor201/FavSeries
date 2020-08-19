import os
import sys, subprocess

# delete created files
os.remove("startUp.bat")

#uninstall librarys
subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', 'pyautogui'])
subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', 'beautifulsoup4'])
subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', 'pywin32'])
