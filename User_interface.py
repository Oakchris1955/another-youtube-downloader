#import tkinter module
from tkinter import *
import tkinter.ttk as ttk

#import threading module
from threading import *

#import the functions module
from functions import *

class MainUI:
	def __init__(self, root):
		self.root = root
		
		#create the download and progress labels
		self.link_label = Label(root, text='Enter the link of the video you wanna download:', width=40)
		self.progress_label = Label(root, text='Not downloading anything right now', width=35)

		#add the entry to get the link
		self.link_entry = Entry(root)

		#add the progress bar
		self.downloadbar = ttk.Progressbar(root, orient = HORIZONTAL, length = 150, maximum=100, mode = 'determinate')

		#add the button
		self.download_button = Button(root, bd=3, text='Start downloading', command=lambda:Thread(target=functions.download_video).start())

		#arrange the widgets
		self.link_label.grid(row=0, column=0, pady = 2)
		self.progress_label.grid(row=1, column=1, pady=2)

		self.link_entry.grid(row=0, column=1, pady=2)

		self.downloadbar.grid(row=1, column=0, pady=2)

		self.download_button.grid(row=2, column=0, columnspan=2)

		#configure the window
		root.columnconfigure(0, weight=1)
		root.columnconfigure(1, weight=1)

		root.rowconfigure(0, weight=1)
		root.rowconfigure(1, weight=1)

		#initialize the function class
		functions = functions_class(self)