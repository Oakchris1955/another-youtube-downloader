#import the Youtube video downloader
from yt_dlp import YoutubeDL, DownloadError

#import the logger
from logger import Logger

#import the time module
from time import time

#import the tkinter module
import tkinter as tk

#import os module to get download folder
import os

class functions_class:
	def __init__(self, UI):
		self.UI = UI
		self.lastupdated = time()

	def update_progressbar(self, response):
		#if bar was updated less than 0.1 seconds ago, don't update
		if time()-self.lastupdated>0.1:
			#check if it is downloading
			if response['status'] == 'downloading' and 'downloaded_bytes' in response and 'total_bytes' in response:
				#calculate percent downloaded
				fragment_downloaded = round(float(response['downloaded_bytes'])/float(response['total_bytes'])*100, 1)
				#update status bar and label
				self.UI.downloadbar['value'] = fragment_downloaded
				progress_text = str(fragment_downloaded)+'% downloaded'
				self.UI.progress_label.config(text=progress_text)
				self.lastupdated = time()
		if response['status'] == 'finished':
			self.UI.progress_label.config(text='Finished downloading')
			self.UI.downloadbar['value'] = 100
			self.UI.root.update_idletasks()


	def download_video(self):
		#disable the button to prevent multiple downloads at once
		self.UI.download_button['state'] = tk.DISABLED

		ydl_opts = {
				'progress_hooks': [self.update_progressbar],
				'outtmpl': '%(title)s.%(ext)s',
				'logger': Logger(self.UI),
				'format':'best',
				'outtmpl': str(os.path.join( os.getenv('USERPROFILE'), 'Downloads'))+'/'+'%(title)s.%(ext)s'
			}
		
		#update the UI so that the button becomes normal again
		self.UI.root.update_idletasks()

		#update the progress label
		self.UI.progress_label.config(text='Processing...')
		self.UI.downloadbar['value'] = 0
		self.UI.root.update()

		#check if the URL given is blank
		if self.UI.link_entry.get() != '':
			with YoutubeDL(ydl_opts) as ydl:
				#also handle any errors
				try:
					ydl.download([self.UI.link_entry.get()])
				except DownloadError:
					self.UI.progress_label.config(text='Non valid URL entered. Please enter a valid URL')
		else:
			self.UI.progress_label.config(text='Please enter an URL')
		
		#re-enable the button
		self.UI.download_button['state'] = tk.NORMAL