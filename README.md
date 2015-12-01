# Browsefolder
A python-curses script to make folder browsing in terminal easier
This script makes folder browing easier in command line
```
Usage: Copy this file into a local folder
       Add the follwing line to your .cshrc/.bashrc
       alias bf 'python /path/to/browsefolder; cd `tail -n 1 ~/.bf`'
       To start the program, enter the command 'bf'
       The following are the keys to control folder movement
       Up and Down            to select folders
       Left or Backspace      to move one folder up
       Right or Tab           to move to the selected folder
       /                      to start search
       Esc                    to clear search
       Enter                  to make the current directory as the working directory in the shell
```
The script will create a temporary file named .bf in your home folder which will contain all the folders that you have browsed to
If the file gets too big, you can delete the file.
