#!/usr/bin/python

import curses
import os

folderlist=[]                       # The global vairable which will hold the list of folders in the current directory
cwd = os.getcwd()                   # Get the active directory
selectedfolderindex = 0             # Index of the folder currently selected in the folder list

screen = curses.initscr()

# Getting the currenct screen size to use in curses refresh
scrSize = screen.getmaxyx()
maxH = scrSize[0] -1
maxW = scrSize[1] -1

# Curses pad to show the current working directory. Will be displayed at the top of the screen
cwdpad = curses.newpad(1,1000)

# Curses pad to show the list of folders in the current working directory.
folderpad = curses.newpad(1000,100)

def listfolders():
    """ Function to list the folders in current working directory. This function will clear and display the curses pads """
    # Making global variable available locally.
    global cwd, folderlist, selectedfolderindex, cwdpad, folderpad, maxW, maxH
    cwdpad.clear()
    folderpad.clear()

    # Add the current working directory string to the pad
    cwdpad.addstr(0,1,cwd,curses.A_BOLD)
    cwdpad.refresh(0,0,0,0,0,maxW) # Update the current working directory display

    # curline variable will keep track of the current line where the next folder name should be added
    curline = 0

    # Looping through the folder list
    for item in folderlist:
        # If the current item is the selected folder, then highlight this item.
        if item == folderlist[selectedfolderindex]:
            folderpad.addstr(curline,0,item,curses.A_REVERSE)
            curline+=1
        else:
            folderpad.addstr(curline,0,item)
            curline+=1
    if selectedfolderindex>maxH-2:
        folderpad.refresh(selectedfolderindex-maxH+1,0,1,0,maxH,maxW)
    else:
        folderpad.refresh(0,0,1,0,maxH,maxW)
    return

def updatefolderlist():
    """ Function to update the folderlist array which will contain the list of folders in the current working directory """
    global cwd, folderlist, selectedfolderindex
    folderlist=[]
    selectedfolderindex=0 # Reset the selected folder index to 0
    for item in os.listdir(cwd):
        if os.path.isdir(item):
            folderlist.append(item)
    folderlist.sort() # Sort the folder list based on their names
    return

curses.noecho()         #no key output
curses.curs_set(0)      #dont display cursor on screen
folderpad.keypad(1)

updatefolderlist()      # Update the folder list for the first time
listfolders()           # List the folder names in the curses pad

# Start key capture to respond to events
while True:
    event = folderpad.getch()

    # If enter is pressed, stop the key capture and proceed with the rest of the code
    if event == 10: 
        break
    # If up arrow is pressed, select the folder one step up
    elif event == 258:
        if selectedfolderindex < len(folderlist) - 1:
            selectedfolderindex+=1
    # if down arrow is pressed, select the folder on step down
    elif event == 259:
        if selectedfolderindex > 0:
            selectedfolderindex-=1
    # if left arrow is pressed, move to the parent folder
    elif event == 260:
        cwd = os.path.dirname(cwd)
        os.chdir(cwd)
        updatefolderlist()

    # if right arrow is pressed, move to the selected (if any) subfolder
    elif event == 261:
        if len(folderlist)>0:
            # checking if there are any subfolders
            if cwd == "/":
                # Checking if this is the root folder
                targetcwd = cwd + folderlist[selectedfolderindex]
            else:
                targetcwd = cwd + "/" + folderlist[selectedfolderindex]
            haveaccess = os.access(targetcwd,os.R_OK) # Checking if the current user has access to the selected folder
            if haveaccess:
                cwd = targetcwd
                os.chdir(cwd)
                updatefolderlist()
            else:
                print('\a') # If no access, emit a bell
    elif event == curses.KEY_RESIZE:
        scrSize = screen.getmaxyx()
        maxH = scrSize[0] -1
        maxW = scrSize[1] -1
    listfolders()       # Update the folder list after capturing the key stroke


curses.endwin()         # Stop the curses window and go back to previous view

# Since python is executed in a separate shell, the selected path needs to be communicated to the shell in some way.
# It is done by writing to a file in the user's home folder
# This should be read by the shell and should do a cd to the selected folder
# python browsefolders; cd `tail -n 1 ~/.bf`
fpath = os.path.expanduser("~/.bf")
with open(fpath, "a+") as f:
    f.write(cwd + "\n")
