#import tkinter module
from tkinter import *
import tkinter.ttk as ttk

#import the Youtube video downloader
from yt_dlp import YoutubeDL

#import other libs
import json, time

#import Classes and UI
from logger import *
import User_interface

#create a window
root = Tk()

#import the UI from User_interface.py
UI = User_interface.MainUI(root)

#show the window
root.mainloop()